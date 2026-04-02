import streamlit as st

# 🔧 Page Config (MUST be first Streamlit command)
st.set_page_config(
    page_title="AI Interview System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ✅ Debug start (helps detect crash)
st.write("App started ✅")

# ==============================
# 🗄️ DATABASE INITIALIZATION
# ==============================
try:
    from db import init_db   # ✅ FIXED IMPORT
    init_db()
    st.success("Database initialized successfully ✅")
except Exception as e:
    st.error(f"Database error ❌: {e}")

# ==============================
# 🎯 MAIN UI
# ==============================
st.title("🎯 AI Interview System")
st.subheader("Intelligent Skill Assessment Platform")

st.markdown("""
Welcome to the AI Interview System!

Use the sidebar to navigate:

- 🏠 **Home** — Start a new interview session  
- 🎤 **Interview** — Live AI-driven interview  
- 📊 **Results** — View your performance report  
- ⚙️ **Admin** — Manage question bank  
""")

# ==============================
# 📊 DASHBOARD METRICS
# ==============================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Interviews Conducted", "—")

with col2:
    st.metric("Avg Score", "—")

with col3:
    st.metric("Domains", "6")

# ==============================
# 📌 FOOTER / INFO
# ==============================
st.markdown("---")
st.info("🚀 System Ready. Use sidebar to begin your interview.")