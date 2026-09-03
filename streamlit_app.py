import streamlit as st
from classifier import classify
import time
from secrets_helper import get_secret

MAX_REQUESTS_PER_MINUTE = 5

if "request_timestamps" not in st.session_state:
    st.session_state.request_timestamps = []


def check_rate_limit() -> bool:
    now = time.time()
    # Keep only timestamps from the last 60 seconds
    st.session_state.request_timestamps = [
        ts for ts in st.session_state.request_timestamps if now - ts < 60
    ]
    if len(st.session_state.request_timestamps) >= MAX_REQUESTS_PER_MINUTE:
        return False
    st.session_state.request_timestamps.append(now)
    return True


# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="EU AI Act Compliance Checker",
    page_icon="🇪🇺",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
  /* Overall background */
  .stApp { background-color: #0f1117; }


  /* Card container */
  .result-card {
      border-radius: 12px;
      padding: 24px 28px;
      margin-top: 20px;
      border-left: 6px solid;
  }
  .card-danger  { background: #2a0f0f; border-color: #e63946; }
  .card-warning { background: #2a1f00; border-color: #f4a261; }
  .card-info    { background: #0a1f2a; border-color: #4cc9f0; }
  .card-success { background: #0f2a0f; border-color: #2dc653; }


  /* Risk level badge */
  .badge {
      display: inline-block;
      padding: 6px 16px;
      border-radius: 999px;
      font-weight: 700;
      font-size: 0.85rem;
      letter-spacing: 0.05em;
      margin-bottom: 12px;
  }
  .badge-danger  { background: #e63946; color: #fff; }
  .badge-warning { background: #f4a261; color: #1a1a1a; }
  .badge-info    { background: #4cc9f0; color: #1a1a1a; }
  .badge-success { background: #2dc653; color: #1a1a1a; }


  /* Verdict text */
  .verdict { font-size: 1.1rem; font-weight: 600; color: #f0f0f0; margin-bottom: 8px; }
  .meta    { font-size: 0.85rem; color: #aaa; margin-bottom: 16px; }


  /* Section labels */
  .section-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #888;
      margin-top: 14px;
      margin-bottom: 4px;
  }
  .section-body { color: #ddd; font-size: 0.95rem; }


  /* Trigger pill */
  .trigger-pill {
      display: inline-block;
      background: #1e1e2e;
      border: 1px solid #444;
      border-radius: 6px;
      padding: 3px 10px;
      font-family: monospace;
      font-size: 0.85rem;
      color: #cba6f7;
  }


  /* Text area label */
  label { color: #ccc !important; font-size: 0.95rem !important; }


  /* Header */
  h1 { font-size: 1.9rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🇪🇺 About this Tool")
    st.markdown(
        "This tool classifies AI use cases against the **EU AI Act** risk framework "
        "(Regulation 2024/1689), covering four tiers:"
    )
    st.markdown("""
- 🔴 **Unacceptable** — Prohibited outright
- 🟠 **High Risk** — Strict conformity obligations
- 🔵 **Limited Risk** — Transparency obligations
- 🟢 **Minimal Risk** — No specific obligations
""")
    st.divider()
    st.markdown("Built by **Shivam Kumar**")
    st.markdown("[GitHub](https://github.com/ShivamKumar20-AI/eu-ai-act-checker) · [LinkedIn](#)")
        # Demo: show if a test secret is configured (no real secret needed)
    test_secret = get_secret("TEST_SECRET", default=None)
    if test_secret:
        st.info("🔐 Secrets loaded from .env (demo mode).")


# ── Main UI ───────────────────────────────────────────────────
st.markdown("# 🇪🇺 EU AI Act Compliance Checker")
st.markdown(
    "<span style='color:#aaa;font-size:0.95rem'>"
    "Describe your AI system below to get an instant risk classification under the EU AI Act."
    "</span>",
    unsafe_allow_html=True,
)
st.markdown("")


use_case = st.text_area(
    "Describe your AI use case:",
    placeholder="e.g. A chatbot that screens job applicants based on CV content and interview responses...",
    height=140,
)


col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    check = st.button("⚡ Check Compliance", use_container_width=True)


# ── Result rendering ──────────────────────────────────────────
CARD_MAP = {
    "badge-danger":  "card-danger",
    "badge-warning": "card-warning",
    "badge-info":    "card-info",
    "badge-success": "card-success",
}


ICON_MAP = {
    "badge-danger":  "🚫",
    "badge-warning": "⚠️",
    "badge-info":    "ℹ️",
    "badge-success": "✅",
}


if check:
    if not use_case.strip():
        st.warning("Please enter a use case description first.")
    elif not check_rate_limit():
        st.error("Too many requests. Please wait a minute before trying again.")
    else:
        with st.spinner("Analysing against EU AI Act framework..."):
            result = classify(use_case)


        badge   = result["badge_class"]
        card    = CARD_MAP.get(badge, "card-success")
        icon    = ICON_MAP.get(badge, "✅")


        st.markdown(f"""
<div class="result-card {card}">
  <span class="badge {badge}">{icon} {result['risk_level']}</span>
  <div class="verdict">{result['verdict']}</div>
  <div class="meta">📋 {result['eu_ai_act_category']}</div>


  <div class="section-label">Why this classification?</div>
  <div class="section-body">{result['why']}</div>


  <div class="section-label">Matched trigger</div>
  <div><span class="trigger-pill">{result['matched_trigger']}</span></div>


  <div class="section-label">Recommendation</div>
  <div class="section-body">{result['recommendation']}</div>
</div>
""", unsafe_allow_html=True)


        # Expander for raw JSON (for technical users / portfolio viewers)
        with st.expander("🔍 View raw classifier output"):
            st.json(result)


# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#555;font-size:0.8rem'>"
    "EU AI Act Compliance Checker · Built with Streamlit · "
    "Not legal advice — for educational and portfolio purposes only."
    "</div>",
    unsafe_allow_html=True,
)