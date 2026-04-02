from config import SKILL_WEIGHTS

def compute_overall_score(evaluations: list) -> float:
    if not evaluations:
        return 0.0
    total = 0.0
    for ev in evaluations:
        weighted = sum(
            ev.get(skill, 0) * weight
            for skill, weight in SKILL_WEIGHTS.items()
        )
        total += weighted
    return round(total / len(evaluations), 2)

def get_skill_averages(evaluations: list) -> dict:
    if not evaluations:
        return {}
    skills = list(SKILL_WEIGHTS.keys())
    return {
        skill: round(sum(e.get(skill, 0) for e in evaluations) / len(evaluations), 1)
        for skill in skills
    }

def get_recommendation(score: float) -> tuple[str, str]:
    if score >= 80:
        return "Strong Hire", "green"
    elif score >= 65:
        return "Hire", "blue"
    elif score >= 50:
        return "Consider", "orange"
    else:
        return "No Hire", "red"