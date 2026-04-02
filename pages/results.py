
from pdf_report import generate_pdf_report

import streamlit as st
import plotly.graph_objects as go
from skill_evaluator import get_recommendation

st.set_page_config(page_title="Results", layout="wide")
st.title("Interview Report")

if "last_total_score" not in st.session_state:
    st.warning("No interview data found. Please complete an interview first.")
    st.stop()

score      = st.session_state.last_total_score
skill_avgs = st.session_state.last_skill_avgs
feedback   = st.session_state.last_feedback
rec, color = get_recommendation(score)

# Score cards
col1, col2, col3 = st.columns(3)
col1.metric("Overall Score",      f"{score:.1f}/100")
col2.metric("Recommendation",     rec)
col3.metric("Questions Answered", len(st.session_state.get("evaluations", [])))

st.divider()

# Radar chart
skills = list(skill_avgs.keys())
values = list(skill_avgs.values())
fig = go.Figure(go.Scatterpolar(
    r=values + [values[0]],
    theta=[s.replace("_", " ").title() for s in skills] + [skills[0].replace("_", " ").title()],
    fill="toself",
    line_color="#7F77DD"
))
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=False, height=400
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("AI Feedback")
st.write(feedback)

st.subheader("Question-by-Question Breakdown")
for i, (q, a, ev) in enumerate(zip(
    st.session_state.get("questions", []),
    st.session_state.get("answers", []),
    st.session_state.get("evaluations", [])
)):
    with st.expander(f"Q{i+1}: {q.get('question','')[:80]}..."):
        st.markdown(f"**Your answer:** {a}")
        st.markdown(f"**Score:** {ev.get('overall_score',0)}/100")
        st.markdown(f"**Strengths:** {', '.join(ev.get('strengths', []))}")
        st.markdown(f"**Improvements:** {', '.join(ev.get('improvements', []))}")

        st.markdown(f"**Ideal answer:** {ev.get('ideal_answer_summary', '')}")
        st.divider()
st.subheader("Download Report")

if st.button("Download PDF Report"):
    pdf_buffer = generate_pdf_report(
        candidate=st.session_state.get("candidate_name", "Candidate"),
        domain=st.session_state.get("domain", ""),
        difficulty=st.session_state.get("difficulty", ""),
        total_score=st.session_state.get("last_total_score", 0),
        skill_avgs=st.session_state.get("last_skill_avgs", {}),
        feedback=st.session_state.get("last_feedback", ""),
        questions=st.session_state.get("questions", []),
        answers=st.session_state.get("answers", []),
        evaluations=st.session_state.get("evaluations", [])
    )
    st.download_button(
        label="Click here to download PDF",
        data=pdf_buffer,
        file_name="interview_report.pdf",
        mime="application/pdf"
    )

    st.markdown(f"**Ideal answer:** {ev.get('ideal_answer_summary', '')}")
