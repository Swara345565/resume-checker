from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(text1, text2):
    emb1 = model.encode(text1, convert_to_tensor=True)
    emb2 = model.encode(text2, convert_to_tensor=True)
    return float(util.cos_sim(emb1, emb2)[0][0])

def score_resume(resume_text, jd_text, must_have_skills):
    # Hard score: % of required skills found
    matches = [s for s in must_have_skills if s.lower() in resume_text.lower()]
    hard_score = len(matches) / len(must_have_skills) if must_have_skills else 0

    # Soft score: semantic similarity
    soft_score = semantic_similarity(resume_text, jd_text)

    # Weighted final score
    final = 0.6*hard_score*100 + 0.4*soft_score*100
    verdict = "High" if final >= 75 else "Medium" if final >= 40 else "Low"

    missing = list(set(must_have_skills) - set(matches))
    return final, verdict, missing
