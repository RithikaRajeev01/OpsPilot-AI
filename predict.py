# ==========================================================
# OPSPILOT AI
# CENTRAL PREDICTION PIPELINE
# ==========================================================

import joblib

from preprocessing import preprocess
from config import MODEL_PATH, THRESHOLD

from agents.agent1 import process_all_shipments
from agents.agent2 import process_all_decisions
from agents.agent3 import process_all_business_values
from agents.agent4 import process_all_ai_reports
from agents.agent5 import process_all_resolution_plans


# ==========================================================
# LOAD TRAINED MODEL
# ==========================================================

model = joblib.load(MODEL_PATH)


# ==========================================================
# RUN COMPLETE OPSPILOT AI PIPELINE
# ==========================================================

def run_pipeline(df):

    # ------------------------------------------------------
    # PREPROCESS
    # ------------------------------------------------------

    processed_df = preprocess(df)

    # ------------------------------------------------------
    # KEEP ONLY MODEL FEATURES
    # ------------------------------------------------------

    processed_df = processed_df[model.feature_names_]

    # ------------------------------------------------------
    # DEBUG
    # ------------------------------------------------------

    print("\n" + "=" * 80)
    print("MODEL PATH")
    print(MODEL_PATH)

    print("\nMODEL FEATURES")
    print(model.feature_names_)

    print("\nDATAFRAME FEATURES")
    print(processed_df.columns.tolist())

    print("\nDATAFRAME SHAPE")
    print(processed_df.shape)

    print("\nCOLUMN TYPES")
    print(processed_df.dtypes)

    print("\nFIRST ROW")
    print(processed_df.iloc[0])

    print("=" * 80)

    # ------------------------------------------------------
    # PREDICT
    # ------------------------------------------------------

    probabilities = model.predict_proba(processed_df)[:, 1]

    predictions = (
        probabilities >= THRESHOLD
    ).astype(int)

    # ------------------------------------------------------
    # SAVE RESULTS
    # ------------------------------------------------------

    results = processed_df.copy()

    results["Delay Probability"] = probabilities

    results["Delay Risk (%)"] = (
        probabilities * 100
    ).round(2)

    results["Predicted Delay"] = predictions

    # ------------------------------------------------------
    # AGENT 1
    # ------------------------------------------------------

    shipment_reports = process_all_shipments(
        results
    )

    # ------------------------------------------------------
    # AGENT 2
    # ------------------------------------------------------

    decision_reports = process_all_decisions(
        shipment_reports
    )

    # ------------------------------------------------------
    # AGENT 3
    # ------------------------------------------------------

    business_reports = process_all_business_values(
        results,
        shipment_reports
    )

    # ------------------------------------------------------
    # AGENT 4
    # ------------------------------------------------------

    try:
        executive_reports = process_all_ai_reports(
            results
        )
    except Exception:
        executive_reports = [
            "AI Executive Summary temporarily unavailable."
        ]

    # ------------------------------------------------------
    # AGENT 5
    # ------------------------------------------------------

    resolution_reports = process_all_resolution_plans(
        shipment_reports,
        decision_reports,
        business_reports
    )

    # ------------------------------------------------------
    # RETURN EVERYTHING
    # ------------------------------------------------------

    return {

        "predictions": results,

        "agent1": shipment_reports,

        "agent2": decision_reports,

        "agent3": business_reports,

        "agent4": executive_reports,

        "agent5": resolution_reports

    }