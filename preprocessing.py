# ==========================================================
# OPSPILOT AI
# PREPROCESSING PIPELINE
# ==========================================================

import pandas as pd


# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [

    "Type",
    "Days for shipment (scheduled)",
    "Benefit per order",
    "Sales per customer",
    "Category Name",
    "Customer City",
    "Customer Country",
    "Customer Segment",
    "Customer State",
    "Department Name",
    "Market",
    "Order City",
    "Order Country",
    "Order Item Discount",
    "Order Item Discount Rate",
    "Order Item Product Price",
    "Order Item Profit Ratio",
    "Order Item Quantity",
    "Sales",
    "Order Item Total",
    "Order Profit Per Order",
    "Order Region",
    "Order State",
    "Product Price",
    "Product Status",
    "Shipping Mode",
    "order date (DateOrders)"

]


# ==========================================================
# VALIDATE CSV
# ==========================================================

def validate_columns(df):

    missing = []

    for column in REQUIRED_COLUMNS:

        if column not in df.columns:

            missing.append(column)

    if len(missing) > 0:

        raise ValueError(

            "Uploaded CSV is missing the following required columns:\n\n"

            + "\n".join(missing)

        )


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def engineer_features(df):

    df = df.copy()

    # ------------------------------------------------------
    # Date Features
    # ------------------------------------------------------

    df["order date (DateOrders)"] = pd.to_datetime(

        df["order date (DateOrders)"],
        errors="coerce"

    )

    df["Order Month"] = (

        df["order date (DateOrders)"]

        .dt.month

    )

    df["Order Weekday"] = (

        df["order date (DateOrders)"]

        .dt.dayofweek

    )

    df["Order Quarter"] = (

        df["order date (DateOrders)"]

        .dt.quarter

    )

    # ------------------------------------------------------
    # Profit Margin
    # ------------------------------------------------------

    df["Profit Margin"] = (

        df["Order Profit Per Order"]

        /

        (df["Sales"] + 1e-6)

    )

    # ------------------------------------------------------
    # Discount Amount
    # ------------------------------------------------------

    df["Discount Amount"] = (

        df["Order Item Product Price"]

        *

        df["Order Item Discount Rate"]

    )

    # ------------------------------------------------------
    # Average Selling Price
    # ------------------------------------------------------

    df["Average Selling Price"] = (

        df["Sales"]

        /

        (df["Order Item Quantity"] + 1e-6)

    )

    # ------------------------------------------------------
    # High Value Order
    # ------------------------------------------------------

    median_sales = df["Sales"].median()

    df["High Value Order"] = (

        df["Sales"] > median_sales

    ).astype(int)

    return df


# ==========================================================
# REMOVE UNUSED COLUMNS
# ==========================================================

def remove_unused_columns(df):

    remove_columns = [

        "Order Id",

        "Order Customer Id",

        "Customer Id",

        "Product Card Id",

        "Product Category Id",

        "Order Item Cardprod Id",

        "Order Item Id",

        "Customer Email",

        "Customer Fname",

        "Customer Lname",

        "Customer Password",

        "Customer Street",

        "Customer Zipcode",

        "Order Zipcode",

        "Latitude",

        "Longitude",

        "Product Description",

        "Product Image",

        "Product Name",

        "Order Status",

        "shipping date (DateOrders)",

        "order date (DateOrders)"

    ]

    df = df.drop(

        columns=remove_columns,

        errors="ignore"

    )

    return df


# ==========================================================
# COMPLETE PREPROCESSING
# ==========================================================

def preprocess(df):

    validate_columns(df)

    df = engineer_features(df)

    df = remove_unused_columns(df)

    return df