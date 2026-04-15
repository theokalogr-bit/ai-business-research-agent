import json
import anthropic
from tools import SEARCH_TOOL, execute_tool
from prompts import RESEARCH_AGENT_SYSTEM


def run_research_agent(client: anthropic.Anthropic, company_name: str, sector: str = "", country: str = "", status_callback=None) -> dict:
    """
    Research Agent: Gathers factual information about a company using web search.
    Returns a structured dict with company facts.
    """
    user_message = f"Research this company: {company_name}"
    if sector:
        user_message += f"\nSector: {sector}"
    if country:
        user_message += f"\nCountry: {country}"
    user_message += "\n\nUse search tools to gather accurate information. Search multiple times if needed."

    messages = [{"role": "user", "content": user_message}]

    if status_callback:
        status_callback("Research Agent: Searching for company information...")

    # Agentic loop — keep going until Claude stops calling tools
    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=RESEARCH_AGENT_SYSTEM,
            tools=[SEARCH_TOOL],
            messages=messages
        )

        # Collect any text content
        text_content = ""
        tool_calls = []
        for block in response.content:
            if block.type == "text":
                text_content += block.text
            elif block.type == "tool_use":
                tool_calls.append(block)

        # If no tool calls, we're done
        if response.stop_reason == "end_turn" or not tool_calls:
            break

        # Execute tool calls and add results to messages
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []
        for tool_call in tool_calls:
            if status_callback:
                status_callback(f"Research Agent: Searching '{tool_call.input.get('query', '')}'...")
            result = execute_tool(tool_call.name, tool_call.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
        messages.append({"role": "user", "content": tool_results})

    # Extract the final JSON from the last assistant response
    final_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            final_text += block.text

    # Try to parse JSON from the response
    try:
        start = final_text.find("{")
        end = final_text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(final_text[start:end])
    except (json.JSONDecodeError, ValueError):
        pass

    # Fallback: return raw text wrapped in a dict
    return {
        "name": company_name,
        "description": final_text,
        "industry": sector or "Unknown",
        "size": "Not found",
        "founded": "Not found",
        "location": country or "Not found",
        "website": "Not found",
        "recent_news": [],
        "key_facts": []
    }
