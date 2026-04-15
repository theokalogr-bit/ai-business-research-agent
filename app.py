import os
import re
import streamlit as st
from datetime import datetime
from pathlib import Path
from orchestrator import run_research_pipeline

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Business Research Agent",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Design System (st.html for CSS injection) ─────────────────────────────────
st.html("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=JetBrains+Mono:wght@300;400;500;600&family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg:        #040911;
    --surface:   #080f1c;
    --card:      #0c1527;
    --border:    #0e2040;
    --border-hi: #1a3a6b;
    --cyan:      #22d3ee;
    --cyan-dim:  #0e7490;
    --cyan-glow: rgba(34,211,238,0.15);
    --orange:    #f97316;
    --green:     #4ade80;
    --muted:     #4b6a8a;
    --text:      #94b8d4;
    --text-hi:   #cde4f5;
    --white:     #e8f4fd;
}
.stApp { background: var(--bg) !important; font-family: 'Outfit', sans-serif !important; }
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse 80% 40% at 50% -10%, rgba(34,211,238,0.06) 0%, transparent 70%), #040911 !important;
}
[data-testid="stHeader"], header[data-testid="stHeader"] { display: none !important; }
.main .block-container { padding: 2.5rem 3rem !important; max-width: 1400px !important; }
hr { border: none !important; border-top: 1px solid var(--border) !important; margin: 1.5rem 0 !important; }
[data-testid="stForm"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 4px !important; padding: 1.5rem !important; }
[data-testid="stTextInput"] label { color: var(--cyan) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.68rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; }
[data-testid="stTextInput"] input { background: var(--surface) !important; border: 1px solid var(--border-hi) !important; border-radius: 3px !important; color: var(--white) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.9rem !important; }
[data-testid="stTextInput"] input:focus { border-color: var(--cyan) !important; box-shadow: 0 0 0 3px var(--cyan-glow) !important; }
[data-testid="stTextInput"] input::placeholder { color: var(--muted) !important; }
[data-testid="stFormSubmitButton"] button { background: transparent !important; border: 1px solid var(--cyan) !important; border-radius: 3px !important; color: var(--cyan) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; font-weight: 600 !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; width: 100% !important; transition: all 0.25s !important; margin-top: 0.5rem !important; }
[data-testid="stFormSubmitButton"] button:hover { background: var(--cyan-glow) !important; box-shadow: 0 0 24px var(--cyan-glow) !important; color: var(--white) !important; }
.stProgress > div { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 2px !important; height: 5px !important; }
.stProgress > div > div { background: linear-gradient(90deg, var(--cyan), #06b6d4) !important; box-shadow: 0 0 10px var(--cyan) !important; border-radius: 2px !important; }
[data-testid="stAlert"] { background: var(--card) !important; border: 1px solid var(--border-hi) !important; border-radius: 3px !important; color: var(--text-hi) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.8rem !important; }
.stInfo { border-left: 3px solid var(--cyan) !important; }
.stSuccess { border-left: 3px solid var(--green) !important; }
.stError { border-left: 3px solid var(--orange) !important; }
[data-testid="metric-container"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 4px !important; padding: 1rem 1.2rem !important; }
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: var(--muted) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.65rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: var(--cyan) !important; font-family: 'Bebas Neue', sans-serif !important; font-size: 1.6rem !important; }
.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; border: none !important; border-bottom: 2px solid transparent !important; color: var(--muted) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.72rem !important; letter-spacing: 0.12em !important; text-transform: uppercase !important; padding: 0.75rem 1.5rem !important; }
.stTabs [aria-selected="true"] { color: var(--cyan) !important; border-bottom-color: var(--cyan) !important; }
.stTabs [data-baseweb="tab-panel"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-top: none !important; padding: 1.5rem !important; border-radius: 0 0 4px 4px !important; }
.stMarkdown h1 { font-family:'Bebas Neue',sans-serif !important; font-size:1.8rem !important; color:var(--white) !important; border-bottom:1px solid var(--border-hi) !important; padding-bottom:0.5rem !important; letter-spacing:0.05em !important; }
.stMarkdown h2 { font-family:'Bebas Neue',sans-serif !important; font-size:1.25rem !important; color:var(--cyan) !important; margin-top:2rem !important; letter-spacing:0.05em !important; }
.stMarkdown h3 { font-size:1rem !important; color:var(--text-hi) !important; font-weight:600 !important; }
.stMarkdown p  { color:var(--text) !important; font-size:0.92rem !important; line-height:1.75 !important; }
.stMarkdown li { color:var(--text) !important; font-size:0.92rem !important; line-height:1.75 !important; }
.stMarkdown strong { color:var(--text-hi) !important; }
.stMarkdown table { border-collapse:collapse !important; width:100% !important; font-family:'JetBrains Mono',monospace !important; font-size:0.78rem !important; }
.stMarkdown th { background:var(--surface) !important; color:var(--cyan) !important; padding:0.6rem 1rem !important; border:1px solid var(--border-hi) !important; letter-spacing:0.1em !important; text-transform:uppercase !important; font-size:0.68rem !important; }
.stMarkdown td { color:var(--text) !important; padding:0.6rem 1rem !important; border:1px solid var(--border) !important; }
.stMarkdown tr:hover td { background:rgba(34,211,238,0.03) !important; }
.stMarkdown code { background:var(--surface) !important; color:var(--cyan) !important; font-family:'JetBrains Mono',monospace !important; padding:0.1rem 0.4rem !important; border-radius:2px !important; }
.stMarkdown em { color:var(--muted) !important; }
.stJson { background: var(--surface) !important; border: 1px solid var(--border) !important; border-radius: 3px !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; }
[data-testid="stDownloadButton"] button { background: transparent !important; border: 1px solid var(--border-hi) !important; border-radius: 3px !important; color: var(--text) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.7rem !important; letter-spacing: 0.15em !important; text-transform: uppercase !important; transition: all 0.2s !important; margin-top: 1rem !important; }
[data-testid="stDownloadButton"] button:hover { border-color: var(--cyan) !important; color: var(--cyan) !important; }
.stCaptionContainer, [data-testid="stCaptionContainer"] { color: var(--muted) !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.68rem !important; }
.stSpinner > div { border-top-color: var(--cyan) !important; }
[data-testid="stExpander"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 3px !important; }
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan-dim); }
</style>
""")

# ── Header ────────────────────────────────────────────────────────────────────
st.html("""
<div style="padding:1rem 0 1.5rem;">
  <p style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#1a3a6b;letter-spacing:0.25em;text-transform:uppercase;margin:0 0 0.5rem;">◈ AI INTELLIGENCE SYSTEM</p>
  <h1 style="font-family:'Bebas Neue',sans-serif;font-size:clamp(2.5rem,6vw,4rem);letter-spacing:0.06em;color:#e8f4fd;margin:0 0 0.25rem;line-height:1;">
    BUSINESS RESEARCH <span style="color:#22d3ee;">AGENT</span>
  </h1>
  <p style="font-family:'Outfit',sans-serif;font-size:0.9rem;color:#4b6a8a;margin:0.5rem 0 0;letter-spacing:0.02em;">
    Three specialized AI agents. One complete intelligence brief.
  </p>
</div>
""")

# ── Pipeline cards ────────────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns([10, 1, 10, 1, 10])

with c1:
    st.html("""
    <div style="background:#0c1527;border:1px solid #0e2040;border-top:2px solid #22d3ee;border-radius:4px;padding:1.2rem 1.4rem;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#22d3ee;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem;">01 — RESEARCH</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;color:#cde4f5;font-weight:600;margin-bottom:0.35rem;">Research Agent</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#4b6a8a;line-height:1.5;">Web search · Company facts · News · Leadership</div>
    </div>
    """)

with c2:
    st.html('<div style="text-align:center;color:#1a3a6b;font-size:1.6rem;padding-top:1.2rem;">›</div>')

with c3:
    st.html("""
    <div style="background:#0c1527;border:1px solid #0e2040;border-top:2px solid #f97316;border-radius:4px;padding:1.2rem 1.4rem;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#f97316;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem;">02 — COMPETITOR</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;color:#cde4f5;font-weight:600;margin-bottom:0.35rem;">Competitor Agent</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#4b6a8a;line-height:1.5;">3–5 rivals · Market position · Differentiators</div>
    </div>
    """)

with c4:
    st.html('<div style="text-align:center;color:#1a3a6b;font-size:1.6rem;padding-top:1.2rem;">›</div>')

with c5:
    st.html("""
    <div style="background:#0c1527;border:1px solid #0e2040;border-top:2px solid #4ade80;border-radius:4px;padding:1.2rem 1.4rem;">
      <div style="font-family:'JetBrains Mono',monospace;font-size:0.58rem;color:#4ade80;letter-spacing:0.2em;text-transform:uppercase;margin-bottom:0.5rem;">03 — ANALYST</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.95rem;color:#cde4f5;font-weight:600;margin-bottom:0.35rem;">Analyst Agent</div>
      <div style="font-family:'Outfit',sans-serif;font-size:0.78rem;color:#4b6a8a;line-height:1.5;">SWOT · Key insights · Outreach angle</div>
    </div>
    """)

st.divider()

# ── Input form ────────────────────────────────────────────────────────────────
with st.form("research_form"):
    col_a, col_b, col_c = st.columns([3, 2, 2])
    with col_a:
        company_name = st.text_input(
            "Company Name *",
            placeholder="e.g. Skroutz, Viva Wallet, OPAP",
            help="Enter any company name — Greek or international"
        )
    with col_b:
        sector = st.text_input(
            "Sector (optional)",
            placeholder="e.g. E-commerce, Fintech, Retail"
        )
    with col_c:
        country = st.text_input(
            "Country (optional)",
            placeholder="e.g. Greece, Germany, USA"
        )

    submitted = st.form_submit_button("INITIATE RESEARCH PIPELINE", type="primary", use_container_width=True)

# ── Run pipeline ──────────────────────────────────────────────────────────────
if submitted:
    if not company_name.strip():
        st.error("Company name is required.")
        st.stop()

    if not os.getenv("ANTHROPIC_API_KEY"):
        st.error("ANTHROPIC_API_KEY not found. Add it to your .env file.")
        st.stop()

    status_placeholder = st.empty()
    progress_bar = st.progress(0)
    progress_steps = {
        "Starting Agent 1: Research Agent": 5,
        "Research Agent: Searching for company information...": 15,
        "Starting Agent 2: Competitor Agent": 45,
        "Competitor Agent: Mapping the competitive landscape...": 55,
        "Starting Agent 3: Analyst Agent": 80,
        "Analyst Agent: Synthesizing data into intelligence brief...": 90,
    }
    _current_progress = [0]

    def update_status(msg: str):
        status_placeholder.info(f"◈  {msg}")
        step = progress_steps.get(msg)
        if step:
            _current_progress[0] = step
            progress_bar.progress(step)
        elif "Searching" in msg:
            _current_progress[0] = min(75, _current_progress[0] + 3)
            progress_bar.progress(_current_progress[0])

    try:
        with st.spinner("Running 3-agent pipeline..."):
            brief, company_data, competitor_data = run_research_pipeline(
                company_name=company_name.strip(),
                sector=sector.strip(),
                country=country.strip(),
                status_callback=update_status
            )

        progress_bar.progress(100)
        status_placeholder.success("◈  Pipeline complete — intelligence brief ready.")

        st.divider()

        competitors_found = len(competitor_data.get("competitors", []))
        news_count = len(company_data.get("recent_news", []))

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Company", company_data.get("name", company_name))
        m2.metric("Industry", company_data.get("industry", sector or "—"))
        m3.metric("Competitors", competitors_found)
        m4.metric("News Items", news_count)

        st.divider()

        tab1, tab2 = st.tabs(["◈  Intelligence Brief", "⬡  Raw Agent Data"])

        with tab1:
            st.markdown(brief)

            filename = re.sub(r'[^\w\-]', '_', company_name.lower()) + f"_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            filepath = output_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(brief)

            with open(filepath, "r", encoding="utf-8") as f:
                st.download_button(
                    label="EXPORT BRIEF AS MARKDOWN",
                    data=f.read(),
                    file_name=filename,
                    mime="text/markdown"
                )

        with tab2:
            col_r, col_cx = st.columns(2)
            with col_r:
                st.subheader("Agent 01 — Company Research")
                st.json(company_data)
            with col_cx:
                st.subheader("Agent 02 — Competitor Analysis")
                st.json(competitor_data)

    except ValueError as e:
        status_placeholder.empty()
        progress_bar.empty()
        st.error(str(e))
    except Exception as e:
        status_placeholder.empty()
        progress_bar.empty()
        st.error(f"Pipeline error: {str(e)}")
        with st.expander("Error details"):
            import traceback
            st.code(traceback.format_exc())

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("◈ AI Business Research Agent  ·  Claude claude-sonnet-4-6  ·  Multi-agent orchestration  ·  Web search")
