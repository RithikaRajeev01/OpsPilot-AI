# ==========================================================
# OPSPILOT AI
# AGENT 2 : ENTERPRISE OPERATIONS DECISION AGENT
# ==========================================================

def operations_decision_agent(report):

    priority = report["Operational Priority"]

    # ------------------------------------------------------
    # Priority 1
    # ------------------------------------------------------

    if priority == "Priority 1 - Immediate Intervention":

        impact = "High"

        recommendation = (
            "Immediate operational intervention is recommended to "
            "reduce delivery disruption risk and maintain customer "
            "service commitments."
        )

        actions = [

            "Escalate the shipment to the Regional Operations Manager.",

            "Prioritize warehouse processing and order fulfillment.",

            "Upgrade transportation to an expedited shipping service.",

            "Initiate proactive customer communication regarding potential delivery delays.",

            "Continuously monitor shipment progress until successful delivery."

        ]

        outcome = (
            "Timely implementation of the recommended actions is expected "
            "to reduce delivery delays, improve customer satisfaction, "
            "and support service-level agreement compliance."
        )

    # ------------------------------------------------------
    # Priority 2
    # ------------------------------------------------------

    elif priority == "Priority 2 - High":

        impact = "Moderate"

        recommendation = (
            "Priority operational review is recommended to minimize "
            "delivery delays and maintain operational efficiency."
        )

        actions = [

            "Prioritize shipment scheduling.",

            "Review warehouse processing capacity.",

            "Monitor transportation progress.",

            "Notify customer support teams of potential delivery delays."

        ]

        outcome = (
            "Early intervention is expected to reduce operational risk "
            "and improve delivery reliability."
        )

    # ------------------------------------------------------
    # Priority 3
    # ------------------------------------------------------

    elif priority == "Priority 3 - Standard Review":

        impact = "Moderate"

        recommendation = (
            "Standard operational monitoring is recommended with "
            "periodic shipment review."
        )

        actions = [

            "Continue standard shipment monitoring.",

            "Review shipment status periodically.",

            "Escalate only if operational conditions change."

        ]

        outcome = (
            "Current operational controls are expected to maintain "
            "acceptable delivery performance."
        )

    # ------------------------------------------------------
    # Priority 4
    # ------------------------------------------------------

    else:

        impact = "Low"

        recommendation = (
            "Routine operational monitoring is sufficient."
        )

        actions = [

            "Continue routine shipment monitoring.",

            "No additional operational intervention is required."

        ]

        outcome = (
            "Current operational performance is expected to remain stable."
        )

    # ------------------------------------------------------
    # Return
    # ------------------------------------------------------

    return {

        "Business Impact Level": impact,

        "Executive Recommendation": recommendation,

        "Recommended Operational Actions": actions,

        "Expected Operational Outcome": outcome

    }


# ==========================================================
# PROCESS ALL SHIPMENTS
# ==========================================================

def process_all_decisions(agent1_reports):

    decisions = []

    for report in agent1_reports:

        decisions.append(

            operations_decision_agent(report)

        )

    return decisions