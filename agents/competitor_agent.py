import json
import anthropic
from tools import SEARCH_TOOL, execute_tool
from prompts import COMPETITOR_AGENT_SYSTEM


def run_competitor_agent(client: anthropic.Anthropic, company_data: dict, status_callback=None) -> dict:
    """
    Competitor Agent: Finds and analyzes 3-5 competitors based on company research data.
    Returns a structured dict with competitor analysis.
    """
    company_name = company_data.get("name", "Unknown")
    industry = company_data.get("industry", "")
    description = company_data.get("description", "")

    user_message = f"""Find competitors for this company:

Company: {company_name}
Industry: {industry}
Description: {description}

Search for their top 3-5 direct competitors and analyze the competitive landscape."""

    messages = [{"role": "user", "content": user_message}]

    if status_callback:
        status_callback("Competitor Agent: Mapping the competitive landscape...")

    # Agentic loop
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=COMPETITOR_AGENT_SYSTEM,
            tools=[SEARCH_TOOL],
            messages=messages
        )

        tool_calls = []
        for block in response.content:
            if block.type == "tool_use":
                tool_calls.append(block)

        if response.stop_reason == "end_turn" or not tool_calls:
            break

        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tool_call in tool_calls:
            if status_callback:
                status_callback(f"Competitor Agent: Searching '{tool_call.input.get('query', '')}'...")
            result = execute_tool(tool_call.name, tool_call.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
        messages.append({"role": "user", "content": tool_results})

    final_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_text += block.text

    try:
        start = final_text.find("{")
        end = final_text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(final_text[start:end])
    except (json.JSONDecodeError, ValueError):
        pass

    return {
        "competitors": [],
        "market_position": final_text
    }
