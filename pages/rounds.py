import streamlit as st
from config import QUESTIONS_PER_INTERVIEW

# 🔧 Page Config
st.set_page_config(page_title="Interview Rounds", layout="wide")

# ✅ Always show something (prevents blank page)
st.title("🎯 Interview Rounds")
st.subheader("Choose your interview round")
st.write("Rounds page loaded ✅")

# ==============================
# 🎤 ROUNDS DATA
# ==============================
rounds = [
    {
        "name": "Technical Round",
        "description": "Tests core technical skills, coding concepts, and problem solving ability.",
        "domain": "Python",
        "difficulty": "Medium",
        "icon": "💻"
    },
    {
        "name": "HR Round",
        "description": "Tests communication, behavioral skills, and cultural fit with the organization.",
        "domain": "Web Development",
        "difficulty": "Easy",
        "icon": "🤝"
    },
    {
        "name": "System Design Round",
        "description": "Tests ability to design large scale systems and software architecture.",
        "domain": "System Design",
        "difficulty": "Hard",
        "icon": "🏗️"
    }
]

st.divider()

# ==============================
# 🎯 SESSION STATE INIT
# ==============================
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

# ==============================
# 📊 DISPLAY ROUNDS
# ==============================
cols = st.columns(3)

for i, r in enumerate(rounds):
    with cols[i]:
        st.markdown(f"## {r['icon']}")
        st.markdown(f"### {r['name']}")
        st.write(r["description"])
        st.caption(f"Domain: {r['domain']}")
        st.caption(f"Difficulty: {r['difficulty']}")
        st.caption(f"Questions: {QUESTIONS_PER_INTERVIEW}")

        st.divider()

        if st.button(f"Start {r['name']}", key=f"btn_{i}", use_container_width=True):
            try:
                # ✅ Show feedback immediately
                st.success(f"Starting {r['name']}...")

                # ✅ Reset session state
                st.session_state.interview_started = False
                st.session_state.current_q_index = 0
                st.session_state.questions = []
                st.session_state.answers = []
                st.session_state.evaluations = []
                st.session_state.asked_questions = []
                st.session_state.candidate_name = st.session_state.get("candidate_name", "")
                st.session_state.domain = r["domain"]
                st.session_state.difficulty = r["difficulty"]
                st.session_state.round_name = r["name"]
                st.session_state.timer_start = None

                # ✅ Safe navigation (Streamlit Cloud compatible)
                st.switch_page("Interview")

            except Exception as e:
                st.error(f"Navigation error ❌: {e}")