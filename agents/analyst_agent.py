import json
from datetime import date
import anthropic
from prompts import ANALYST_AGENT_SYSTEM


def run_analyst_agent(client: anthropic.Anthropic, company_data: dict, competitor_data: dict, status_callback=None) -> str:
    """
    Analyst Agent: Synthesizes research and competitor data into a full business intelligence brief.
    Returns a Markdown string.
    """
    if status_callback:
        status_callback("Analyst Agent: Synthesizing data into intelligence brief...")

    today = date.today().strftime("%B %d, %Y")

    user_message = f"""Synthesize this data into a full business intelligence brief.

Today's date: {today}

COMPANY RESEARCH DATA:
{json.dumps(company_data, indent=2)}

COMPETITOR ANALYSIS DATA:
{json.dumps(competitor_data, indent=2)}

Produce the full Markdown brief now. Be specific and analytical — use the actual data above."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=ANALYST_AGENT_SYSTEM,
        messages=[{"role": "user", "content": user_message}]
    )

    return response.content[0].text
