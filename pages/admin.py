
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("Admin Panel")
st.subheader("Interview Management")

from db import get_all_interviews

st.markdown("### All Interviews")

try:
    interviews = get_all_interviews()
    if interviews:
        for iv in interviews:
            with st.expander(f"{iv['candidate']} — {iv['domain']} — Score: {iv['total_score']}"):
                st.write(f"Difficulty: {iv['difficulty']}")
                st.write(f"Date: {iv['created_at']}")
                st.write(f"Feedback: {iv['feedback']}")
                if iv['skill_scores']:
                    scores = json.loads(iv['skill_scores']) if isinstance(iv['skill_scores'], str) else iv['skill_scores']
                    st.json(scores)
    else:
        st.info("No interviews conducted yet.")
except Exception as e:
    st.error(f"Error loading interviews: {e}")

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json

st.set_page_config(page_title="Admin Panel", layout="wide")
st.title("Admin Panel")
st.subheader("Interview Management")

from db import get_all_interviews

st.markdown("### All Interviews")

try:
    interviews = get_all_interviews()
    if interviews:
        for iv in interviews:
            with st.expander(f"{iv['candidate']} — {iv['domain']} — Score: {iv['total_score']}"):
                st.write(f"Difficulty: {iv['difficulty']}")
                st.write(f"Date: {iv['created_at']}")
                st.write(f"Feedback: {iv['feedback']}")
                if iv['skill_scores']:
                    scores = json.loads(iv['skill_scores']) if isinstance(iv['skill_scores'], str) else iv['skill_scores']
                    st.json(scores)
    else:
        st.info("No interviews conducted yet.")
except Exception as e:
    st.error(f"Error loading interviews: {e}")

