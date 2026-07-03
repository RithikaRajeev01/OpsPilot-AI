# ==========================================================
# OPSPILOT AI
# ENTERPRISE APPLICATION
# ==========================================================

from flask import (
    Flask,
    render_template,
    request
)

import os
import pandas as pd

from config import (
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS
)

from predict import run_pipeline


# ==========================================================
# FLASK APP
# ==========================================================

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ==========================================================
# CREATE UPLOAD FOLDER
# ==========================================================

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# ==========================================================
# ALLOWED FILE
# ==========================================================

def allowed_file(filename):

    return (

        "." in filename

        and

        filename.rsplit(".", 1)[1].lower()

        in

        ALLOWED_EXTENSIONS

    )


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(

        "index.html",

        critical=0,

        avg_risk="0%",

        revenue="$0",
        
        revenue_numeric=0,

        total=0,

        potential_savings="$0",
        
        potential_savings_numeric=0,

        critical_percentage=0,

        table=None,

        executive=None,

        resolution=None,

        high_risk=0,
        
        intervention_window=None,
        
        risk_drivers=None,

        critical_count=0,

        high_count=0,

        medium_count=0,

        low_count=0,
        
        error_message=None

    )


# ==========================================================
# PREDICT
# ==========================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # ------------------------------------------------------
    # Validate Upload
    # ------------------------------------------------------

    if "file" not in request.files:

        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":

        return "Please select a CSV file."

    if not allowed_file(file.filename):

        return "Only CSV files are supported."

    # ------------------------------------------------------
    # Save Uploaded CSV
    # ------------------------------------------------------

    filepath = os.path.join(

        app.config["UPLOAD_FOLDER"],

        file.filename

    )

    file.save(filepath)

    # ------------------------------------------------------
    # Read CSV
    # ------------------------------------------------------

    try:

        df = pd.read_csv(

            filepath,

            encoding="utf-8"

        )

    except UnicodeDecodeError:

        df = pd.read_csv(

            filepath,

            encoding="latin-1"

        )

    except Exception:

        df = pd.read_csv(

            filepath,

            encoding="cp1252"

        )

    # ------------------------------------------------------
    # Run AI Pipeline
    # ------------------------------------------------------

    results = run_pipeline(df)

    prediction_df = results["predictions"]

    # --- ADDED: Priority Score Logic ---
    prediction_df["Priority Score"] = (
        prediction_df["Delay Risk (%)"] * 0.7 +
        (prediction_df["Sales"] / prediction_df["Sales"].max()) * 30
    ).round(1)

    # ======================================================
    # TOP 100 PRIORITY SHIPMENTS
    # ======================================================

    top100 = prediction_df.sort_values(

        "Priority Score",

        ascending=False

    ).head(100)

    agent1 = results["agent1"]

    agent2 = results["agent2"]

    agent3 = results["agent3"]

    agent4 = results["agent4"]

    agent5 = results["agent5"]

    # ------------------------------------------------------
    # KPI
    # ------------------------------------------------------

    total_shipments = len(prediction_df)

    # Use Top 100 length for Immediate Action Queue
    critical_shipments = len(top100)

    average_risk = round(

        prediction_df["Delay Risk (%)"].mean(),

        2

    )

    # ======================================================
    # FINANCIAL EXPOSURE (TOP 100 ONLY)
    # ======================================================

    revenue = round(

        top100["Sales"].sum(),

        2

    )

    potential_savings = round(

        revenue * 0.15,

        2

    )

    high_shipments = min(
        300,
        len(
            prediction_df[
                (prediction_df["Delay Risk (%)"] >= 60) &
                (prediction_df["Delay Risk (%)"] < 80)
            ]
        )
    )

    intervention_window = "Within 2 Hours"

    risk_drivers = (

        "First-Class Shipments, Low Scheduled Delivery Time, "

        "High Revenue Orders"

    )

    critical_percentage = round(

        (critical_shipments / total_shipments) * 100,

        1

    ) if total_shipments else 0

    # ------------------------------------------------------
    # SHIPMENT RISK DISTRIBUTION
    # ------------------------------------------------------
    
    critical_count = len(
        prediction_df[
            prediction_df["Delay Risk (%)"] >= 80
        ]
    )
    
    high_count = len(
        prediction_df[
            (prediction_df["Delay Risk (%)"] >= 60)
            &
            (prediction_df["Delay Risk (%)"] < 80)
        ]
    )
    
    medium_count = len(
        prediction_df[
            (prediction_df["Delay Risk (%)"] >= 40)
            &
            (prediction_df["Delay Risk (%)"] < 60)
        ]
    )
    
    low_count = len(
        prediction_df[
            prediction_df["Delay Risk (%)"] < 40
        ]
    )

    # ======================================================
    # PRIORITY LABEL
    # ======================================================

    prediction_df["Priority"] = prediction_df["Delay Risk (%)"].apply(

        lambda x:

            "🔴 Immediate Action" if x >= 80 else

            "🟠 High Priority" if x >= 60 else

            "🟡 Monitor" if x >= 40 else

            "🟢 Normal"

    )


    # ======================================================
    # RECOMMENDED ACTION
    # ======================================================

    prediction_df["Recommended Action"] = prediction_df["Delay Risk (%)"].apply(

        lambda x:

            "Immediate Intervention"

            if x >= 80

            else

            "Expedite Shipment"

            if x >= 60

            else

            "Increase Monitoring"

            if x >= 40

            else

            "Routine Monitoring"

    )


    # ======================================================
    # SORT BY PRIORITY SCORE FIRST (CHANGED)
    # ======================================================

    prediction_df = prediction_df.sort_values(

        "Priority Score",

        ascending=False

    )


    # ======================================================
    # DISPLAY ONLY IMPORTANT COLUMNS
    # ======================================================

    display_df = prediction_df[

        [

            "Order City",

            "Order Country",

            "Shipping Mode",

            "Sales",

            "Priority Score",

            "Delay Risk (%)",

            "Priority",

            "Recommended Action"

        ]

    ].head(10)


    table = display_df.to_html(

        classes="table table-hover table-striped",

        index=False,

        escape=False

    )

    # ------------------------------------------------------
    # AI REPORTS
    # ------------------------------------------------------

    executive = (

        agent4[0]

        if len(agent4) > 0

        else

        "No Executive AI Report Generated."

    )

    resolution = (

        agent5[0]

        if len(agent5) > 0

        else

        "No Resolution Plan Generated."

    )

    # ------------------------------------------------------
    # DYNAMIC DISPLAY FORMATTING (REVENUE & SAVINGS)
    # ------------------------------------------------------

    if revenue >= 1000000:
        revenue_display = f"${revenue/1000000:.2f}M"
    elif revenue >= 1000:
        revenue_display = f"${revenue/1000:.1f}K"
    else:
        revenue_display = f"${revenue:,.0f}"

    if potential_savings >= 1000000:
        savings_display = f"${potential_savings/1000000:.2f}M"
    elif potential_savings >= 1000:
        savings_display = f"${potential_savings/1000:.1f}K"
    else:
        savings_display = f"${potential_savings:,.0f}"


    # ------------------------------------------------------
    # RENDER DASHBOARD
    # ------------------------------------------------------

    return render_template(

        "index.html",

        critical=critical_shipments,

        avg_risk=f"{average_risk}%",

        revenue=revenue_display,
        
        revenue_numeric=revenue,

        total=total_shipments,

        critical_percentage=critical_percentage,

        table=table,

        executive=executive,

        resolution=resolution,

        potential_savings=savings_display,
        
        potential_savings_numeric=potential_savings,

        high_risk=high_shipments,

        intervention_window=intervention_window,

        risk_drivers=risk_drivers,

        critical_count=critical_count,

        high_count=high_count,

        medium_count=medium_count,

        low_count=low_count,
        
        error_message=None

    )


# ==========================================================
# ERROR HANDLER
# ==========================================================

@app.errorhandler(Exception)
def handle_error(error):
    
    # Print it to terminal for you to see easily
    print(f"CRITICAL ERROR: {str(error)}") 

    return render_template(

        "index.html",

        critical=0,

        avg_risk="0%",

        revenue="$0",
        
        revenue_numeric=0,

        total=0,

        potential_savings="$0",
        
        potential_savings_numeric=0,

        critical_percentage=0,

        table=None,

        executive=f"❌ {str(error)}",

        resolution="The requested operation could not be completed.",
        
        high_risk=0,
        
        intervention_window=None,
        
        risk_drivers=None,

        critical_count=0,

        high_count=0,

        medium_count=0,

        low_count=0,
        
        error_message=str(error)

    )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )