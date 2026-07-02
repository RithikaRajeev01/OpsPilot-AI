# ==========================================================
# OPSPILOT AI
# AGENT 5 : ENTERPRISE OPERATIONAL ACTION PLAN
# HACKATHON VERSION
# ==========================================================

def enterprise_resolution_agent(report, decision, business):

    actions = [
        "Assign shipment to Priority Operations Desk",
        "Contact logistics carrier and confirm shipment status",
        "Validate revised estimated delivery time (ETA)",
        "Escalate shipment if SLA threshold is exceeded",
        "Notify customer of any ETA changes",
        "Close case after delivery confirmation"
    ]

    html = f"""

<h3>Recommended Enterprise Workflow</h3>

<hr>

<h4>Execution Checklist</h4>

<ul>

{''.join(f'<li>{x}</li>' for x in actions)}

</ul>

"""

    return html

# ==========================================================
# PROCESS RESOLUTION PLANS
# HACKATHON VERSION
# ONLY ONE PLAN
# ==========================================================

def process_all_resolution_plans(
    agent1_reports,
    agent2_reports,
    agent3_reports
):
    if (
        len(agent1_reports) == 0
        or len(agent2_reports) == 0
        or len(agent3_reports) == 0
    ):
        return ["<p style='color: var(--ink-500);'>No operational data available to generate a resolution plan.</p>"]

    plan = enterprise_resolution_agent(
        agent1_reports[0],
        agent2_reports[0],
        agent3_reports[0]
    )

    # Wrap the return string in a list so app.py can safely call [0] on it
    return [plan]