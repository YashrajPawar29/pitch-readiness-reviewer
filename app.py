"""Pitch Readiness Reviewer - Streamlit app.

Run with:  streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from pitchreview import ai
from pitchreview.scorer import review

SAMPLES = {p.stem: p for p in sorted((Path(__file__).parent / "sample_pitches").glob("*.md"))}

st.set_page_config(page_title="Pitch Readiness Reviewer", page_icon="🎤", layout="wide")
st.title("🎤 Pitch Readiness Reviewer")
st.caption("Score a startup pitch the way an angel investor would - and get the coaching "
           "questions to close the gaps before demo day.")

with st.sidebar:
    st.header("Pitch")
    choice = st.selectbox("Start from a sample", ["(my own pitch)"] + list(SAMPLES))
    upload = st.file_uploader("...or upload a script (.md / .txt)", type=["md", "txt"])
    st.divider()
    mode_ai = st.toggle("Ask Claude to judge too", value=False,
                        disabled=not ai.is_available(),
                        help="Set ANTHROPIC_API_KEY to enable. Offline rubric is used otherwise.")

default = ""
if upload is not None:
    default = upload.read().decode("utf-8", errors="ignore")
elif choice in SAMPLES:
    default = SAMPLES[choice].read_text()

pitch = st.text_area("Pitch script or one-pager", default, height=260,
                     placeholder="Paste your pitch here...")
if not pitch.strip():
    st.info("Paste a pitch, upload one, or pick a sample from the sidebar.")
    st.stop()

report = review(pitch)

c1, c2, c3 = st.columns(3)
c1.metric("Readiness score", f"{report.total}/100")
c2.metric("Red flags", len(report.red_flags))
c3.metric("Words", report.word_count)
st.subheader(report.verdict)

df = pd.DataFrame([{"Criterion": s.criterion.name, "Weight": s.criterion.weight,
                    "Score (1-5)": s.score, "Signals found": ", ".join(s.matched) or "-",
                    "Judges look for": s.criterion.looks_for} for s in report.scores])
left, right = st.columns([3, 2])
with left:
    st.dataframe(df, use_container_width=True, hide_index=True)
with right:
    st.bar_chart(df.set_index("Criterion")["Score (1-5)"], horizontal=True)

tab_gaps, tab_flags, tab_ai = st.tabs(["🧭 Biggest gaps", "🚩 Red flags", "🤖 Claude as judge"])

with tab_gaps:
    for s in report.weakest():
        st.markdown(f"**{s.criterion.name}** - scored {s.score}/5")
        for q in s.criterion.questions:
            st.markdown(f"- {q}")

with tab_flags:
    if not report.red_flags:
        st.success("No common red-flag phrases found.")
    for f in report.red_flags:
        st.error(f"**{f['flag']}** - “{f['found']}”  \n{f['advice']}")

with tab_ai:
    if not mode_ai:
        st.info("Turn on **Ask Claude to judge too** in the sidebar (needs an API key). "
                "Claude scores each criterion with quotes from your pitch and drafts the "
                "questions a judge panel is likely to ask.")
    elif st.button("Get Claude's verdict", type="primary"):
        with st.spinner("The judge is reading your pitch..."):
            try:
                result = ai.judge(pitch)
            except Exception as e:  # show the error in the UI rather than crash
                st.error(str(e))
                st.stop()
        st.dataframe(pd.DataFrame(result["scores"]), use_container_width=True,
                     hide_index=True)
        st.success(f"**Strongest point:** {result['strongest_point']}")
        st.warning(f"**Biggest risk:** {result['biggest_risk']}")
        st.markdown("**Second meeting?** " +
                    ("Yes" if result["would_take_a_second_meeting"] else "Not yet"))
        st.markdown("### Questions to expect from judges")
        for q in result["judge_questions"]:
            st.markdown(f"- {q}")
        st.markdown("### Next steps")
        for q in result["next_steps"]:
            st.markdown(f"- {q}")
