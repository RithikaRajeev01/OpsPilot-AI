# ==========================================================
# OPSPILOT AI
# AGENT 1 : ENTERPRISE SHIPMENT RISK PREDICTION
# ==========================================================

def shipment_prediction_agent(shipment):

    probability = float(shipment["Delay Probability"])

    # ------------------------------------------------------
    # Risk Classification
    # ------------------------------------------------------

    if probability >= 0.80:

        risk = "Critical Risk"
        priority = "Priority 1 - Immediate Intervention"
        business_index = 79.0
        sla = "Immediate Operational Escalation"

    elif probability >= 0.60:

        risk = "High Risk"
        priority = "Priority 2 - High"
        business_index = 65.0
        sla = "Priority Operational Review"

    elif probability >= 0.40:

        risk = "Moderate Risk"
        priority = "Priority 3 - Standard Review"
        business_index = 50.0
        sla = "Standard Operational Monitoring"

    else:

        risk = "Low Risk"
        priority = "Priority 4 - Routine Monitoring"
        business_index = 30.0
        sla = "Routine Monitoring"

    # ------------------------------------------------------
    # Root Causes
    # ------------------------------------------------------

    causes = []

    if shipment["Days for shipment (scheduled)"] >= 5:
        causes.append("Extended scheduled delivery timeline")

    if shipment["High Value Order"] == 1:
        causes.append("High-value commercial shipment")

    if shipment["Shipping Mode"] == "Standard Class":
        causes.append("Standard transportation service selected")

    if len(causes) == 0:
        causes.append("No significant operational risk factors identified")

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "Delay Probability": round(probability, 4),

        "Delay Risk (%)": round(probability * 100, 2),

        "Delivery Risk Classification": risk,

        "Operational Priority": priority,

        "Business Priority Index": business_index,

        "Recommended Service Response": sla,

        "Primary Risk Drivers": causes

    }


# ==========================================================
# PROCESS ENTIRE CSV
# ==========================================================

def process_all_shipments(results_df):

    reports = []

    for _, shipment in results_df.iterrows():

        reports.append(

            shipment_prediction_agent(shipment)

        )

    return reports