import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import streamlit as st
from groq_service import (
    generate_round_question,
    generate_adaptive_round_question,
    evaluate_answer,
    generate_final_feedback,
    detect_ai_answer
)
from skill_evaluator import compute_overall_score, get_skill_averages, get_recommendation
from db import save_interview, save_session
from config import DOMAINS, DIFFICULTY_LEVELS, QUESTIONS_PER_INTERVIEW

st.set_page_config(page_title="Interview Room", layout="wide")
st.title("Interview Room")

# -------------------------------
# SESSION DEFAULTS
# -------------------------------
defaults = {
    "interview_started": False,
    "current_q_index": 0,
    "questions": [],
    "answers": [],
    "evaluations": [],
    "asked_questions": [],
    "candidate_name": "",
    "domain": "",
    "difficulty": "",
    "round_name": "Technical Round",
    "timer_start": None,
    "timer_q_index": -1,
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -------------------------------
# SETUP SCREEN
# -------------------------------
if not st.session_state.interview_started:
    st.subheader("Setup Your Interview")

    with st.form("setup_form"):
        name = st.text_input("Your Name")
        domain = st.selectbox("Domain", DOMAINS)
        difficulty = st.selectbox("Difficulty", DIFFICULTY_LEVELS)
        submitted = st.form_submit_button("Start Interview")

    if submitted and name:
        st.session_state.candidate_name = name
        st.session_state.domain = domain
        st.session_state.difficulty = difficulty
        st.session_state.interview_started = True
        st.rerun()

# -------------------------------
# INTERVIEW FLOW
# -------------------------------
else:
    idx = st.session_state.current_q_index
    total = QUESTIONS_PER_INTERVIEW

    st.progress(idx / total, text=f"Question {idx + 1} of {total}")
    st.caption(
        f"Candidate: {st.session_state.candidate_name} | "
        f"Round: {st.session_state.round_name} | "
        f"Domain: {st.session_state.domain} | "
        f"Difficulty: {st.session_state.difficulty}"
    )

    if idx < total:

        # -------------------------------
        # GENERATE QUESTION
        # -------------------------------
        if len(st.session_state.questions) <= idx:
            with st.spinner("Generating next question..."):
                try:
                    if st.session_state.evaluations:
                        avg_score = sum(
                            e.get("overall_score", 0)
                            for e in st.session_state.evaluations
                        ) / len(st.session_state.evaluations)

                        q_data = generate_adaptive_round_question(
                            st.session_state.round_name,
                            st.session_state.domain,
                            st.session_state.difficulty,
                            st.session_state.asked_questions,
                            avg_score
                        )

                        if st.session_state.round_name == "Technical Round":
                            adjusted = q_data.get("adjusted_difficulty", st.session_state.difficulty)
                            if adjusted != st.session_state.difficulty:
                                st.info(f"Difficulty adjusted to {adjusted} based on your performance!")

                    else:
                        q_data = generate_round_question(
                            st.session_state.round_name,
                            st.session_state.domain,
                            st.session_state.difficulty,
                            st.session_state.asked_questions
                        )

                except Exception as e:
                    st.error(f"Error generating question: {e}")
                    st.stop()

            if not q_data or "question" not in q_data:
                st.error("Failed to generate question. Retrying...")
                st.rerun()

            st.session_state.questions.append(q_data)
            st.session_state.asked_questions.append(q_data["question"])
            st.session_state.timer_start = time.time()
            st.session_state.timer_q_index = idx

        # -------------------------------
        # DISPLAY QUESTION
        # -------------------------------
        q_data = st.session_state.questions[idx]
        question_text = q_data.get("question")

        if not question_text:
            st.error("Question not available")
            st.stop()

        st.markdown(f"### Q{idx + 1}. {question_text}")
        st.caption(f"Expected topics: {', '.join(q_data.get('expected_topics', []))}")

        # -------------------------------
        # TIMER
        # -------------------------------
        if st.session_state.timer_start:
            time_limit = 120
            elapsed = time.time() - st.session_state.timer_start
            remaining = max(0, time_limit - int(elapsed))

            mins = remaining // 60
            secs = remaining % 60

            if remaining > 30:
                st.success(f"Time remaining: {mins:02d}:{secs:02d}")
            elif remaining > 10:
                st.warning(f"Time remaining: {mins:02d}:{secs:02d}")
            else:
                st.error(f"Time remaining: {mins:02d}:{secs:02d}")

            if remaining == 0:
                st.warning("Time is up! Auto submitting...")

                st.session_state.answers.append("No answer - time expired")
                st.session_state.evaluations.append({
                    "domain_knowledge": 0,
                    "problem_solving": 0,
                    "communication": 0,
                    "completeness": 0,
                    "overall_score": 0,
                    "strengths": [],
                    "improvements": ["Did not answer within time limit"],
                    "ideal_answer_summary": "No answer provided",
                    "verdict": "Needs Improvement"
                })

                st.session_state.current_q_index += 1
                st.session_state.timer_start = None
                st.rerun()

        # -------------------------------
        # ANSWER FORM
        # -------------------------------
        with st.form(f"answer_form_{idx}"):
            answer = st.text_area(
                "Your Answer",
                height=200,
                placeholder="Type your detailed answer here..."
            )
            submitted = st.form_submit_button("Submit Answer")

        # -------------------------------
        # EVALUATE ANSWER + AI DETECTION
        # -------------------------------
        if submitted and answer.strip():

            # 🚨 AI Detection
            with st.spinner("Checking answer authenticity..."):
                detection = detect_ai_answer(answer)

            if "AI" in detection:
                st.error("⚠️ AI-generated answer detected! Please answer in your own words.")
                st.stop()

            # ✅ Evaluate Answer
            with st.spinner("Evaluating your answer..."):
                try:
                    evaluation = evaluate_answer(
                        question=question_text,
                        answer=answer,
                        domain=st.session_state.domain,
                        expected_topics=q_data.get("expected_topics", [])
                    )
                except Exception as e:
                    st.error(f"Error evaluating answer: {e}")
                    st.stop()

            st.session_state.answers.append(answer)
            st.session_state.evaluations.append(evaluation)
            st.session_state.current_q_index += 1
            st.session_state.timer_start = None

            score = evaluation.get("overall_score", 0)
            verdict = evaluation.get("verdict", "")

            if score >= 70:
                st.success(f"Score: {score}/100 — {verdict}")
            elif score >= 50:
                st.warning(f"Score: {score}/100 — {verdict}")
            else:
                st.error(f"Score: {score}/100 — {verdict}")

            st.rerun()

        time.sleep(1)
        st.rerun()

    # -------------------------------
    # FINAL REPORT
    # -------------------------------
    else:
        st.success("Interview complete! Generating your report...")

        total_score = compute_overall_score(st.session_state.evaluations)
        skill_avgs = get_skill_averages(st.session_state.evaluations)

        with st.spinner("Generating final feedback..."):
            try:
                feedback = generate_final_feedback(
                    st.session_state.domain,
                    st.session_state.evaluations,
                    total_score
                )
            except Exception as e:
                st.error(f"Error generating feedback: {e}")
                st.stop()

        interview_id = save_interview(
            candidate=st.session_state.candidate_name,
            domain=st.session_state.domain,
            difficulty=st.session_state.difficulty,
            total_score=total_score,
            skill_scores=skill_avgs,
            feedback=feedback
        )

        for q, a, ev in zip(
            st.session_state.questions,
            st.session_state.answers,
            st.session_state.evaluations
        ):
            save_session(interview_id, q.get("question", ""), a, ev)

        st.session_state.last_interview_id = interview_id
        st.session_state.last_total_score = total_score
        st.session_state.last_skill_avgs = skill_avgs
        st.session_state.last_feedback = feedback

        recommendation, _ = get_recommendation(total_score)

        st.metric("Overall Score", f"{total_score:.1f} / 100")
        st.info(f"Recommendation: **{recommendation}**")

        st.switch_page("pages/results.py")