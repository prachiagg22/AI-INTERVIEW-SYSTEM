import os
try:
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_MODEL = "llama-3.3-70b-versatile"

DOMAINS = ["Python", "Web Development", "Data Structures & Algorithms",
           "Machine Learning", "SQL & Databases", "System Design"]
DIFFICULTY_LEVELS = ["Easy", "Medium", "Hard"]
QUESTIONS_PER_INTERVIEW = 3
SKILL_WEIGHTS = {
    "domain_knowledge": 0.40,
    "problem_solving":  0.30,
    "communication":    0.20,
    "completeness":     0.10,
}