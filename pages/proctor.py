import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Proctored Interview", layout="wide")
st.title("Proctored Interview Mode")

if "proctor_warnings" not in st.session_state:
    st.session_state.proctor_warnings = 0

if "proctor_terminated" not in st.session_state:
    st.session_state.proctor_terminated = False

# Check termination
if st.session_state.proctor_terminated:
    st.error("Your interview has been terminated due to too many violations!")
    st.metric("Total Violations", st.session_state.proctor_warnings)
    st.stop()

# Warning display
col1, col2, col3 = st.columns(3)
col1.metric("Warnings", f"{st.session_state.proctor_warnings}/3")
col2.metric("Status", "Active")
col3.metric("Mode", "Proctored")

if st.session_state.proctor_warnings >= 3:
    st.session_state.proctor_terminated = True
    st.error("Interview terminated — too many violations!")
    st.rerun()

# Proctoring JavaScript
components.html("""
<script>
let warned = false;

document.addEventListener('visibilitychange', function() {
    if (document.hidden && !warned) {
        warned = true;
        alert('Warning: You switched tabs! This has been recorded.');
        // Send message to parent Streamlit
        window.parent.postMessage({type: 'TAB_SWITCH'}, '*');
        setTimeout(() => { warned = false; }, 3000);
    }
});

window.addEventListener('blur', function() {
    document.title = 'WARNING: Return to Interview!';
});

window.addEventListener('focus', function() {
    document.title = 'Proctored Interview';
});

document.addEventListener('contextmenu', function(e) {
    e.preventDefault();
    alert('Right-click disabled during interview.');
});
</script>
<div style="background:#fff3cd;padding:12px;border-radius:8px;
border:1px solid #ffc107;font-family:sans-serif;font-size:14px;">
    <b>Proctoring Active</b> — Tab switching and right-click are monitored.
    Violations are recorded.
</div>
""", height=70)

st.divider()
st.warning("Do NOT switch tabs during the interview. Each violation is recorded.")

# Manual violation button for testing
col1, col2 = st.columns(2)
if col1.button("Simulate Tab Switch (Test)"):
    st.session_state.proctor_warnings += 1
    st.warning(f"Violation recorded! Warnings: {st.session_state.proctor_warnings}/3")
    st.rerun()

if col2.button("Start Proctored Interview"):
    st.session_state.interview_started = False
    st.session_state.current_q_index = 0
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.evaluations = []
    st.session_state.asked_questions = []

    st.switch_page("pages/interview.py")

    st.switch_page("pages/interview.py")

