<<<<<<< HEAD
=======

>>>>>>> 3f4fcfae6056b8a8090aeac73e6cb21a77bf8185
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from resume_parser import extract_text_from_pdf
from groq_service import analyze_resume

st.set_page_config(page_title="Resume Analysis", layout="wide")
st.title("Resume Upload & AI Analysis")
st.subheader("Upload your resume to get personalized interview questions")

uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

if uploaded_file:
    with st.spinner("Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text:
        st.error("Could not read the PDF. Please try another file.")
        st.stop()

    st.success("Resume uploaded successfully!")

    with st.spinner("Analyzing your resume with AI..."):
        analysis = analyze_resume(resume_text)

    if not analysis:
        st.error("Could not analyze resume. Please try again.")
        st.stop()

    st.divider()

    # Show analysis results
    col1, col2, col3 = st.columns(3)
    col1.metric("Candidate", analysis.get("candidate_name", "Unknown"))
    col2.metric("Experience", f"{analysis.get('experience_years', 0)} years")
    col3.metric("Education", analysis.get("education", "N/A"))

    st.subheader("Skills Detected")
    skills = analysis.get("skills", [])
    cols = st.columns(4)
    for i, skill in enumerate(skills):
        cols[i % 4].success(skill)

    st.subheader("AI Recommendations")
    col1, col2 = st.columns(2)
    col1.info(f"Suggested Domain: **{analysis.get('suggested_domain', 'Python')}**")
    col2.info(f"Suggested Difficulty: **{analysis.get('suggested_difficulty', 'Medium')}**")

    st.subheader("Key Strengths")
    for strength in analysis.get("key_strengths", []):
        st.write(f"- {strength}")

    st.subheader("Suggested Interview Topics")
    for topic in analysis.get("suggested_topics", []):
        st.write(f"- {topic}")

    st.divider()

    # Save to session and go to interview
    if st.button("Start Personalized Interview Based on Resume"):
        st.session_state.candidate_name = analysis.get("candidate_name", "Candidate")
        st.session_state.domain = analysis.get("suggested_domain", "Python")
        st.session_state.difficulty = analysis.get("suggested_difficulty", "Medium")
        st.session_state.resume_skills = skills
        st.session_state.interview_started = True
        st.session_state.current_q_index = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.evaluations = []
        st.session_state.asked_questions = []
        st.switch_page("pages/interview.py")




