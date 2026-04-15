# AI Business Research Agent

> A multi-agent AI system that researches any company and produces a complete business intelligence brief — competitive analysis, SWOT, and a specific outreach angle — in minutes.

> **Note:** This is a portfolio project. To run it you need your own API keys (`ANTHROPIC_API_KEY` required). No keys are included in this repo — your credentials are never at risk.

## What This Does

Given a company name, three specialized AI agents collaborate sequentially to produce a structured intelligence brief that would take a human analyst 2–3 hours to produce manually. Each agent has a distinct role and passes structured data to the next. The final output includes company overview, competitive landscape, SWOT analysis, and a tailored outreach recommendation.

Built to demonstrate production-grade multi-agent orchestration using the Claude API with real-time web search and tool use.

## How It Works

```
Input: Company Name + optional Sector / Country
         │
         ▼
┌─────────────────────┐
│  Agent 1: Research  │  Searches the web for company facts, recent news, leadership
└────────┬────────────┘
         │ Structured JSON
         ▼
┌──────────────────────────┐
│  Agent 2: Competitor     │  Identifies 3–5 direct competitors, maps market position
└────────┬─────────────────┘
         │ Structured JSON
         ▼
┌──────────────────────────┐
│  Agent 3: Analyst        │  Synthesizes everything → full brief + SWOT + outreach angle
└────────┬─────────────────┘
         │
         ▼
Output: Markdown intelligence brief (viewable in UI + downloadable)
```

Each agent runs an autonomous agentic loop — it decides what to search, runs multiple queries, and returns structured data before handing off to the next agent.

## Tech Stack

| Component | Technology |
|---|---|
| LLM | Claude claude-sonnet-4-6 (Anthropic) |
| Agent Framework | Custom Python orchestrator (no LangChain) |
| Tool Use | Claude API native tool use |
| Web Search | DuckDuckGo |
| UI | Streamlit |
| Language | Python 3.10+ |

## Setup

```bash
# 1. Clone
git clone https://github.com/theokalogr-bit/ai-business-research-agent
cd ai-business-research-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env — add your ANTHROPIC_API_KEY (required)
# Optionally add TAVILY_API_KEY for better search results

# 4. Run
streamlit run app.py
```

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | Yes | Your Anthropic API key |
| `TAVILY_API_KEY` | Yes | Your Tavily API key |

## Example Output

**Input:** Company: `Skroutz` / Sector: `E-commerce` / Country: `Greece`

**[View the full generated brief →](skroutz_20260415_0352.md)**

Selected highlights from the output:

- Calculated take rate of ~1.5% ($27.2M revenue vs ~$1.8B GMV) — flagged as anomalous, signaling either heavy reinvestment or revenue recognition conservatism
- Named Head of Commercial (Yiota Tzavara) as the specific outreach decision-maker
- Quantified the Temu threat: Chinese platforms captured ~40% of Greek e-commerce turnover (€529–627M, 2024)
- Identified Cyprus as international expansion template after 97% YoY Black Friday growth
- Specific outreach angle: *"Lead with merchant catalog normalization and dynamic pricing AI — Skroutz's growth depends on merchant onboarding velocity, which is a manual process today"*

This brief was generated in a single pipeline run with no manual editing.

## Use Cases

- **Sales & BD teams** — research any prospect company before a call, in minutes instead of hours
- **AI automation consultants** — generate client research briefs as part of pre-engagement discovery
- **Investors & analysts** — quick competitive intelligence on any company in any market

## Architecture Decisions

**Why no LangChain?**
Custom orchestrator keeps every agent interaction explicit and readable. Better for debugging, easier to extend, and more impressive to technical reviewers than a black-box framework.

**Why sequential agents instead of parallel?**
Agent 2 depends on Agent 1's output. Agent 3 depends on both. The dependency chain is real — sequential execution preserves data quality through the pipeline.

**Why Tavily with DuckDuckGo fallback?**
Tavily gives significantly better business research results. DuckDuckGo requires no API key and serves as a free fallback, making the system usable out of the box.

---

Built by [Theo](https://github.com/theokalogr-bit) — AI automation consultant based in Greece.
