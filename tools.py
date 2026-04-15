import os
import requests
from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> str:
    """Search the web. Uses Tavily if API key is available, falls back to DuckDuckGo."""
    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key:
        return _tavily_search(query, max_results, tavily_key)
    return _ddg_search(query, max_results)


def _tavily_search(query: str, max_results: int, api_key: str) -> str:
    """Search using Tavily API — better quality results for business research."""
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={"query": query, "max_results": max_results, "search_depth": "basic"},
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=15
        )
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if not results:
            return "No results found."
        formatted = []
        for r in results:
            formatted.append(f"Title: {r.get('title', '')}\nURL: {r.get('url', '')}\nSnippet: {r.get('content', '')}\n")
        return "\n---\n".join(formatted)
    except Exception as e:
        return _ddg_search(query, max_results)


def _ddg_search(query: str, max_results: int) -> str:
    """Fallback: DuckDuckGo search."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return "No results found."
        formatted = []
        for r in results:
            formatted.append(f"Title: {r.get('title', '')}\nURL: {r.get('href', '')}\nSnippet: {r.get('body', '')}\n")
        return "\n---\n".join(formatted)
    except Exception as e:
        return f"Search error: {str(e)}"


# Tool definitions for Claude API tool use
SEARCH_TOOL = {
    "name": "web_search",
    "description": "Search the web for information about a company, industry, or topic. Returns titles, URLs, and snippets from search results.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to use"
            },
            "max_results": {
                "type": "integer",
                "description": "Number of results to return (default 5, max 10)",
                "default": 5
            }
        },
        "required": ["query"]
    }
}


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result."""
    if tool_name == "web_search":
        return web_search(
            query=tool_input["query"],
            max_results=tool_input.get("max_results", 5)
        )
    return f"Unknown tool: {tool_name}"
