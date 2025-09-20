from sentence_transformers import SentenceTransformer, util

# Load model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_semantic_score(resume_text: str, jd_text: str) -> float:
    """Compute semantic similarity between resume and job description"""
    resume_emb = embedding_model.encode(resume_text, convert_to_tensor=True)
    jd_emb = embedding_model.encode(jd_text, convert_to_tensor=True)
    similarity = util.cos_sim(resume_emb, jd_emb)
    return float(similarity[0][0])

def evaluate_resume(resume: dict, jd: dict) -> dict:
    """
    Evaluate resume against JD
    resume: {"skills": [...], "full_text": "..."}
    jd: {"must_have_skills": [...], "full_text": "..."}
    Returns: {"score": float, "verdict": str, "missing_skills": [...], "improvement_suggestions": [...]}
    """

    # 1. Hard match: skills overlap
    resume_skills = set([s.lower() for s in resume.get("skills", [])])
    jd_skills = set([s.lower() for s in jd.get("must_have_skills", [])])

    matched_skills = resume_skills & jd_skills
    hard_score = len(matched_skills) / len(jd_skills) if jd_skills else 0

    # 2. Soft match: semantic similarity
    soft_score = compute_semantic_score(resume.get("full_text", ""), jd.get("full_text", ""))

    # 3. Weighted final score
    final_score = 0.6 * hard_score * 100 + 0.4 * soft_score * 100

    # 4. Verdict mapping
    if final_score >= 75:
        verdict = "High"
    elif final_score >= 40:
        verdict = "Medium"
    else:
        verdict = "Low"

    # 5. Missing skills & suggestions
    missing_skills = list(jd_skills - matched_skills)
    improvement_suggestions = [f"Add skill: {s.capitalize()}" for s in missing_skills]

    return {
        "score": round(final_score, 2),
        "verdict": verdict,
        "missing_skills": missing_skills,
        "improvement_suggestions": improvement_suggestions
    }

# Example usage
if __name__ == "__main__":
    sample_resume = {
        "skills": ["Python", "SQL", "Machine Learning"],
        "full_text": "Experienced in Python, SQL, and Machine Learning projects."
    }

    sample_jd = {
        "must_have_skills": ["Python", "SQL", "Excel"],
        "full_text": "Looking for a candidate skilled in Python, SQL, Excel, and data analysis."
    }

    result = evaluate_resume(sample_resume, sample_jd)
    print(result)
