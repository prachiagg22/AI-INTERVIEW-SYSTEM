import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import json
import pandas as pd
from db import get_all_interviews

st.set_page_config(page_title="Leaderboard", layout="wide")
st.title("Leaderboard")
st.subheader("Top Performing Candidates")

try:
    interviews = get_all_interviews()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

if not interviews:
    st.info("No interviews conducted yet. Be the first!")
    st.stop()

# Build dataframe
rows = []
for iv in interviews:
    skill_scores = {}
    if iv["skill_scores"]:
        try:
            skill_scores = json.loads(iv["skill_scores"]) if isinstance(iv["skill_scores"], str) else iv["skill_scores"]
        except:
            pass

    rows.append({
        "Rank": 0,
        "Candidate": iv["candidate"],
        "Domain": iv["domain"],
        "Difficulty": iv["difficulty"],
        "Overall Score": iv["total_score"],
        "Domain Knowledge": skill_scores.get("domain_knowledge", 0),
        "Problem Solving": skill_scores.get("problem_solving", 0),
        "Communication": skill_scores.get("communication", 0),
        "Date": iv["created_at"][:10],
    })

df = pd.DataFrame(rows)
df = df.sort_values("Overall Score", ascending=False).reset_index(drop=True)
df["Rank"] = df.index + 1

# Add medals
def add_medal(rank):
    if rank == 1: return "1"
    if rank == 2: return "2"
    if rank == 3: return "3"
    return str(rank)

df["Rank"] = df["Rank"].apply(add_medal)

# Top 3 cards
st.subheader("Top 3 Candidates")
top3 = df.head(3)
cols = st.columns(3)
medals = ["1st Place", "2nd Place", "3rd Place"]
colors_list = ["gold", "silver", "#cd7f32"]

for i, (_, row) in enumerate(top3.iterrows()):
    with cols[i]:
        st.markdown(f"### {medals[i]}")
        st.metric(row["Candidate"], f"{row['Overall Score']}/100")
        st.caption(f"Domain: {row['Domain']}")
        st.caption(f"Difficulty: {row['Difficulty']}")
        st.caption(f"Date: {row['Date']}")

st.divider()

# Full leaderboard table
st.subheader("Full Rankings")

# Filters
col1, col2 = st.columns(2)
domain_filter = col1.selectbox("Filter by Domain", ["All"] + list(df["Domain"].unique()))
difficulty_filter = col2.selectbox("Filter by Difficulty", ["All", "Easy", "Medium", "Hard"])

filtered_df = df.copy()
if domain_filter != "All":
    filtered_df = filtered_df[filtered_df["Domain"] == domain_filter]
if difficulty_filter != "All":
    filtered_df = filtered_df[filtered_df["Difficulty"] == difficulty_filter]

st.dataframe(
    filtered_df[[
        "Rank", "Candidate", "Domain", "Difficulty",
        "Overall Score", "Domain Knowledge",
        "Problem Solving", "Communication", "Date"
    ]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# Stats
st.subheader("Overall Statistics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Interviews", len(df))
col2.metric("Highest Score", f"{df['Overall Score'].max()}/100")
col3.metric("Average Score", f"{df['Overall Score'].mean():.1f}/100")
<<<<<<< HEAD
col4.metric("Domains Covered", df["Domain"].nunique())
=======
col4.metric("Domains Covered", df["Domain"].nunique())
>>>>>>> 3f4fcfae6056b8a8090aeac73e6cb21a77bf8185
