from groq import Groq
from dotenv import load_dotenv
import os, json, re, time

# Load environment variables
load_dotenv()

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# -------------------------------
# SAFE API CALL (with retry)
# -------------------------------
def _call_groq(prompt: str) -> str:
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a strict technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024,
            )
            return response.choices[0].message.content

        except Exception as e:
            if attempt < 2:
                time.sleep(2)
            else:
                return f'{{"error": "API failed: {str(e)}"}}'


# -------------------------------
# EXTRACT JSON SAFELY
# -------------------------------
def _extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except:
                return {}
    return {}


# -------------------------------
# GENERATE QUESTION
# -------------------------------
def generate_question(domain: str, difficulty: str, asked_questions: list) -> dict:
    asked_str = "\n".join(f"- {q}" for q in asked_questions[-5:]) or "None"

    prompt = f"""
You are a senior technical interviewer.

Rules:
- Do NOT repeat previous questions
- Ask realistic interview-level questions
- Increase difficulty gradually
- Be specific and practical

Domain: {domain}
Difficulty: {difficulty}

Already asked:
{asked_str}

Respond ONLY in JSON:
{{
  "question": "your question here",
  "expected_topics": ["topic1", "topic2"],
  "sample_answer_hints": ["hint1", "hint2"],
  "difficulty": "{difficulty}"
}}
"""

    text = _call_groq(prompt)
    result = _extract_json(text)

    return result or {
        "question": f"Explain a key concept in {domain}",
        "expected_topics": [],
        "sample_answer_hints": [],
        "difficulty": difficulty
    }


# -------------------------------
# EVALUATE ANSWER
# -------------------------------
def evaluate_answer(question: str, answer: str, domain: str, expected_topics: list) -> dict:
    topics_str = ", ".join(expected_topics)

    prompt = f"""
You are a strict technical interviewer.

Evaluate the candidate honestly (DO NOT give full marks easily).

Domain: {domain}
Question: {question}
Expected topics: {topics_str}
Candidate Answer: {answer}

Scoring rules:
- Be critical
- Average answer = 50-70
- Excellent = 80+
- Weak = below 50

Respond ONLY in JSON:
{{
  "domain_knowledge": 0-100,
  "problem_solving": 0-100,
  "communication": 0-100,
  "completeness": 0-100,
  "overall_score": 0-100,
  "strengths": ["point"],
  "improvements": ["point"],
  "ideal_answer_summary": "short ideal answer",
  "verdict": "Good / Average / Needs Improvement"
}}
"""

    text = _call_groq(prompt)
    result = _extract_json(text)

    return result or {
        "domain_knowledge": 50,
        "problem_solving": 50,
        "communication": 50,
        "completeness": 50,
        "overall_score": 50,
        "strengths": ["Could not evaluate properly"],
        "improvements": ["Try again"],
        "ideal_answer_summary": "N/A",
        "verdict": "Average"
    }


# -------------------------------
# FINAL FEEDBACK
# -------------------------------
def generate_final_feedback(domain: str, all_scores: list, total_score: float) -> str:
    if not all_scores:
        return "No data available."

    avg_scores = {
        k: round(sum(s.get(k, 0) for s in all_scores) / len(all_scores), 1)
        for k in ["domain_knowledge", "problem_solving", "communication"]
    }

    prompt = f"""
You are a senior HR and technical lead.

A candidate completed a {domain} interview.

Overall Score: {total_score:.1f}/100
Skill Breakdown: {avg_scores}

Write:
- 4-5 line professional feedback
- Strength summary
- Weakness summary
- Hiring recommendation
"""

    return _call_groq(prompt)


# -------------------------------
# RESUME ANALYSIS
# -------------------------------
def analyze_resume(resume_text: str) -> dict:
    prompt = f"""You are an expert HR analyst and technical recruiter.
Analyze this resume and extract key information.

Resume:
{resume_text[:3000]}

Respond ONLY in this JSON format:
{{
  "candidate_name": "name from resume",
  "skills": ["skill1", "skill2", "skill3"],
  "experience_years": 2,
  "education": "highest degree",
  "suggested_domain": "Python or Web Development or Machine Learning etc",
  "suggested_difficulty": "Easy or Medium or Hard",
  "key_strengths": ["strength1", "strength2"],
  "suggested_topics": ["topic1", "topic2", "topic3"]
}}"""
    text = _call_groq(prompt)
    return _extract_json(text)


# -------------------------------
# RESUME-BASED QUESTION
# -------------------------------
def generate_resume_based_question(domain: str, difficulty: str, resume_skills: list, asked_questions: list) -> dict:
    asked_str = "\n".join(f"- {q}" for q in asked_questions[-3:]) or "None yet"
    skills_str = ", ".join(resume_skills[:5])

    prompt = f"""You are a senior technical interviewer.
The candidate has these skills from their resume: {skills_str}
Generate ONE {difficulty} level interview question for domain: {domain}
Make the question relevant to their actual skills.

Already asked:
{asked_str}

Respond ONLY in this JSON format:
{{
  "question": "your question here",
  "expected_topics": ["topic1", "topic2"],
  "sample_answer_hints": ["hint1", "hint2"],
  "difficulty": "{difficulty}"
}}"""
    text = _call_groq(prompt)
    return _extract_json(text)


# -------------------------------
# ADAPTIVE QUESTION
# -------------------------------
def generate_adaptive_question(domain: str, difficulty: str, asked_questions: list, avg_score: float) -> dict:
    if avg_score >= 80:
        adjusted_difficulty = "Hard"
    elif avg_score >= 60:
        adjusted_difficulty = "Medium"
    else:
        adjusted_difficulty = "Easy"

    asked_str = "\n".join(f"- {q}" for q in asked_questions[-3:]) or "None yet"

    prompt = f"""You are a senior technical interviewer.
The candidate's current average score is {avg_score:.1f}/100.
Based on performance, generate ONE {adjusted_difficulty} level question for: {domain}

Already asked:
{asked_str}

Respond ONLY in this JSON format:
{{
  "question": "your question here",
  "expected_topics": ["topic1", "topic2"],
  "sample_answer_hints": ["hint1", "hint2"],
  "difficulty": "{adjusted_difficulty}"
}}"""

    text = _call_groq(prompt)
    result = _extract_json(text)

    if not result:
        result = {
            "question": f"Explain a key concept in {domain}",
            "expected_topics": [],
            "sample_answer_hints": [],
            "difficulty": adjusted_difficulty
        }

    result["adjusted_difficulty"] = adjusted_difficulty
    return result
def generate_hr_question(asked_questions: list) -> dict:
    asked_str = "\n".join(f"- {q}" for q in asked_questions[-3:]) or "None yet"
    prompt = f"""You are an experienced HR interviewer.
Generate ONE behavioral or situational interview question.
Already asked:
{asked_str}
Respond ONLY in this JSON format:
{{
  "question": "your HR question here",
  "expected_topics": ["communication", "teamwork"],
  "sample_answer_hints": ["use STAR method"],
  "difficulty": "Easy"
}}"""
    text = _call_groq(prompt)
    return _extract_json(text)

def generate_system_design_question(asked_questions: list) -> dict:
    asked_str = "\n".join(f"- {q}" for q in asked_questions[-3:]) or "None yet"
    prompt = f"""You are a senior system design interviewer.
Generate ONE system design interview question.
Already asked:
{asked_str}
Respond ONLY in this JSON format:
{{
  "question": "your system design question here",
  "expected_topics": ["scalability", "database", "architecture"],
  "sample_answer_hints": ["think about scale", "consider trade-offs"],
  "difficulty": "Hard"
}}"""
    text = _call_groq(prompt)
    return _extract_json(text)
# -------------------------------
# 🎯 ROUND-BASED QUESTION ROUTER
# -------------------------------
def generate_round_question(round_name, domain, difficulty, asked_questions):
    if round_name == "HR Round":
        return generate_hr_question(asked_questions)

    elif round_name == "System Design Round":
        return generate_system_design_question(asked_questions)

    else:  # Technical Round
        return generate_question(domain, difficulty, asked_questions)


# -------------------------------
# 🔁 ADAPTIVE ROUND QUESTION
# -------------------------------
def generate_adaptive_round_question(round_name, domain, difficulty, asked_questions, avg_score):
    
    if round_name == "HR Round":
        return generate_hr_question(asked_questions)

    elif round_name == "System Design Round":
        return generate_system_design_question(asked_questions)

    else:
        return generate_adaptive_question(domain, difficulty, asked_questions, avg_score)
    # -------------------------------
# 🚨 AI CHEATING DETECTION
# -------------------------------
def detect_ai_answer(answer: str) -> str:
    prompt = f"""
    You are an AI detection system.

    Analyze the following answer and determine if it is:
    - Human-written
    - AI-generated
    - Uncertain

    Answer:
    {answer}

    Respond ONLY with one word:
    Human OR AI OR Uncertain
    """

    result = _call_groq(prompt)
    return result.strip()