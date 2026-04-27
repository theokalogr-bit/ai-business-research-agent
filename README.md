# AI Business Research Agent

> A multi-agent AI system that researches any company and generates a full business intelligence brief — in minutes, not hours.

Most sales teams and consultants spend 2-3 hours manually researching a company before an important meeting or pitch. This system does it in under 5 minutes. Give it a company name and it returns a complete brief: background, competitors, SWOT analysis, and outreach recommendations — ready to use.

## Demo

> Demo GIF coming soon — see [Setup](#setup) to run locally.

## How It Works

Three sequential agents, each building on the last:

```
Company Name
     │
     ▼
Research Agent → web search → company facts, news, leadership
     │
     ▼
Competitor Agent → identifies 3-5 direct competitors, maps positioning
     │
     ▼
Analyst Agent → synthesizes into full brief with SWOT + outreach recommendations
     │
     ▼
Streamlit UI → formatted, readable output
```

No LangChain. Pure Python orchestration — transparent, fast, and easy to modify.

## Tech Stack

| Component | Role |
|-----------|------|
| Claude Sonnet 4.6 | All three agents — research, analysis, synthesis |
| DuckDuckGo Search | Web search (no API key needed) |
| Tavily API | Optional — improves search result quality |
| Streamlit | Browser UI |
| Python 3.10+ | Orchestration layer |

## Setup

```bash
git clone https://github.com/theokalogr-bit/ai-business-research-agent
cd ai-business-research-agent
pip install -r requirements.txt
cp .env.example .env
# Add your ANTHROPIC_API_KEY (optional: TAVILY_API_KEY)
streamlit run app.py
```

## Example

**Input:** Skroutz (Greek e-commerce platform)

**Output:**
- Company overview, revenue estimates, key executives
- 4 direct competitors with positioning analysis
- SWOT analysis
- Recommended outreach angle for sales or partnership

## Use Cases

- **Sales teams** — research any prospect before a call, automatically
- **Consultants** — generate client briefings without manual research
- **Investors** — rapid company screening before deeper due diligence

---
Built by [Theo](https://github.com/theokalogr-bit) — AI automation consultant based in Athens, Greece.
