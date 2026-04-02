
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from db import get_all_interviews

st.set_page_config(page_title="AI Interview System", layout="wide")

st.title("AI Interview System")
st.subheader("Intelligent Skill Assessment Platform")

st.markdown("Welcome to the AI-powered interview system.")

try:
    interviews = get_all_interviews()
    total_interviews = len(interviews)
    scores = [i["total_score"] for i in interviews if i["total_score"] is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
except Exception as e:
    st.error(f"DB error: {e}")
    total_interviews = 0
    avg_score = 0

col1, col2, col3 = st.columns(3)
col1.metric("Interviews Conducted", total_interviews)
col2.metric("Avg Score", f"{avg_score}/100" if avg_score else "—")
col3.metric("Domains Available", "6")

st.divider()

st.markdown("### How it works")
st.markdown("""
1. Go to the **Interview** page from the sidebar
2. Enter your name and select domain and difficulty  
3. Answer the AI-generated questions
4. Get your score and detailed feedback on the **Results** page
""")

st.info("Click on **Interview** in the sidebar to start!")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from db import get_all_interviews

st.set_page_config(page_title="AI Interview System", layout="wide")

st.title("AI Interview System")
st.subheader("Intelligent Skill Assessment Platform")

st.markdown("Welcome to the AI-powered interview system.")

try:
    interviews = get_all_interviews()
    total_interviews = len(interviews)
    scores = [i["total_score"] for i in interviews if i["total_score"] is not None]
    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
except Exception as e:
    st.error(f"DB error: {e}")
    total_interviews = 0
    avg_score = 0

col1, col2, col3 = st.columns(3)
col1.metric("Interviews Conducted", total_interviews)
col2.metric("Avg Score", f"{avg_score}/100" if avg_score else "—")
col3.metric("Domains Available", "6")

st.divider()

st.markdown("### How it works")
st.markdown("""
1. Go to the **Interview** page from the sidebar
2. Enter your name and select domain and difficulty  
3. Answer the AI-generated questions
4. Get your score and detailed feedback on the **Results** page
""")

st.info("Click on **Interview** in the sidebar to start!")
