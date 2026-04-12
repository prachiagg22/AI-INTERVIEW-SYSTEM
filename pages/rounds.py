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