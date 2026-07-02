# ==========================================================
# OPSPILOT AI
# AGENT 3 : ENTERPRISE BUSINESS VALUE ASSESSMENT AGENT
# ==========================================================

def business_value_agent(shipment, report):

    sales = float(shipment["Sales"])

    profit = float(shipment["Order Profit Per Order"])

    probability = report["Delay Probability"]

    business_index = report["Business Priority Index"]

    # ------------------------------------------------------
    # Revenue Exposure
    # ------------------------------------------------------

    revenue_exposure = round(

        sales * probability,

        2

    )

    # ------------------------------------------------------
    # Profit Exposure
    # ------------------------------------------------------

    profit_exposure = round(

        max(profit, 0) * probability,

        2

    )

    # ------------------------------------------------------
    # Operational Cost Avoidance
    # ------------------------------------------------------

    operational_cost_avoidance = round(

        revenue_exposure * 0.08,

        2

    )

    # ------------------------------------------------------
    # Expected SLA Improvement
    # ------------------------------------------------------

    if probability >= 0.80:

        sla = "15–20% Improvement"

    elif probability >= 0.60:

        sla = "10–15% Improvement"

    elif probability >= 0.40:

        sla = "5–10% Improvement"

    else:

        sla = "Operational Performance Expected to Remain Stable"

    # ------------------------------------------------------
    # Customer Service Impact
    # ------------------------------------------------------

    if business_index >= 90:

        customer = "Critical Business Impact"

    elif business_index >= 75:

        customer = "High Business Impact"

    elif business_index >= 50:

        customer = "Moderate Business Impact"

    else:

        customer = "Low Business Impact"

    # ------------------------------------------------------
    # Business Value Classification
    # ------------------------------------------------------

    if business_index >= 90:

        value = "Strategic"

    elif business_index >= 75:

        value = "High"

    elif business_index >= 50:

        value = "Moderate"

    else:

        value = "Standard"

    # ------------------------------------------------------
    # Executive Assessment
    # ------------------------------------------------------

    if business_index >= 90:

        assessment = (
            "Immediate operational intervention is expected to deliver "
            "significant business value by reducing financial exposure, "
            "protecting customer commitments, and strengthening "
            "service-level agreement compliance."
        )

    elif business_index >= 75:

        assessment = (
            "Proactive operational management is expected to reduce "
            "delivery risk, protect commercial performance, and "
            "improve operational resilience."
        )

    elif business_index >= 50:

        assessment = (
            "Continued operational monitoring is recommended to maintain "
            "delivery performance within established business thresholds."
        )

    else:

        assessment = (
            "Current operational controls are considered sufficient to "
            "support expected business performance."
        )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "Business Value Classification": value,

        "Potential Revenue Exposure ($)": revenue_exposure,

        "Potential Profit Exposure ($)": profit_exposure,

        "Estimated Operational Cost Avoidance ($)": operational_cost_avoidance,

        "Expected SLA Performance Improvement": sla,

        "Customer Service Impact": customer,

        "Executive Business Assessment": assessment

    }


# ==========================================================
# PROCESS ALL SHIPMENTS
# ==========================================================

def process_all_business_values(results_df, agent1_reports):

    business_reports = []

    for (_, shipment), report in zip(results_df.iterrows(), agent1_reports):

        business_reports.append(

            business_value_agent(

                shipment,

                report

            )

        )

    return business_reports