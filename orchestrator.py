import os
import anthropic
from dotenv import load_dotenv
from agents.research_agent import run_research_agent
from agents.competitor_agent import run_competitor_agent
from agents.analyst_agent import run_analyst_agent

load_dotenv()


def run_research_pipeline(
    company_name: str,
    sector: str = "",
    country: str = "",
    status_callback=None
) -> tuple[str, dict, dict]:
    """
    Orchestrates all 3 agents sequentially:
    1. Research Agent → gathers company facts
    2. Competitor Agent → maps the competitive landscape
    3. Analyst Agent → synthesizes into a full brief

    Returns: (brief_markdown, company_data, competitor_data)
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set. Add it to your .env file.")

    client = anthropic.Anthropic(api_key=api_key)

    # Agent 1: Research
    if status_callback:
        status_callback("Starting Agent 1: Research Agent")
    company_data = run_research_agent(
        client=client,
        company_name=company_name,
        sector=sector,
        country=country,
        status_callback=status_callback
    )

    # Agent 2: Competitor analysis
    if status_callback:
        status_callback("Starting Agent 2: Competitor Agent")
    competitor_data = run_competitor_agent(
        client=client,
        company_data=company_data,
        status_callback=status_callback
    )

    # Agent 3: Synthesis
    if status_callback:
        status_callback("Starting Agent 3: Analyst Agent")
    brief = run_analyst_agent(
        client=client,
        company_data=company_data,
        competitor_data=competitor_data,
        status_callback=status_callback
    )

    return brief, company_data, competitor_data
