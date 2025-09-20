import sqlite3
from datetime import datetime
import streamlit as st
from backend.parse_resume import parse_resume
from backend.parse_jd import parse_jd
from backend.scoring import evaluate_resume

st.set_page_config(page_title="📄 Automated Resume Relevance Checker", layout="wide")
st.title("📄 Automated Resume Relevance Checker")

# ---------- SQLite Setup ----------
DB_FILE = "resume_checker.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        jd_role TEXT,
        resume_text TEXT,
        jd_text TEXT,
        score REAL,
        verdict TEXT,
        missing_skills TEXT,
        improvement_suggestions TEXT,
        timestamp TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()  # ensure DB and table exist

# ---------- Functions ----------
def save_candidate_to_db(name, jd_role, resume_text, jd_text, result):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates
        (name, jd_role, resume_text, jd_text, score, verdict, missing_skills, improvement_suggestions, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        jd_role,
        resume_text,
        jd_text,
        result["score"],
        result["verdict"],
        ",".join(result["missing_skills"]),
        ",".join(result["improvement_suggestions"]),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, jd_role, score, verdict, timestamp FROM candidates ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

# ---------- File Upload ----------
st.subheader("Upload Job Description and Resume")
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

if jd_file and resume_file:
    # Parse JD
    jd = parse_jd(jd_file)
    st.write(f"**Role:** {jd['role']}")
    st.write(f"**Must-Have Skills:** {', '.join(jd['must_have_skills']) if jd['must_have_skills'] else 'None'}")
    st.write(f"**Good-to-Have Skills:** {', '.join(jd['good_to_have_skills']) if jd['good_to_have_skills'] else 'None'}")

    # Parse Resume
    resume = parse_resume(resume_file)

    # Candidate name (simple default, can improve by parsing from resume)
    candidate_name = "Candidate"

    # Evaluate Resume
    result = evaluate_resume(resume, jd)

    st.subheader("✅ Evaluation Results")
    st.write(f"**Relevance Score:** {result['score']:.2f}")
    st.write(f"**Verdict:** {result['verdict']}")
    st.write(f"**Missing Skills:** {', '.join(result['missing_skills']) if result['missing_skills'] else 'None'}")
    st.write("**Improvement Suggestions:**")
    for sug in result['improvement_suggestions']:
        st.write(f"- {sug}")

    # Save to DB
    save_candidate_to_db(candidate_name, jd['role'], resume['full_text'], jd['full_text'], result)
    st.success("✅ Candidate evaluation saved to database!")

# ---------- Display Past Candidates ----------
st.subheader("📋 Past Candidate Evaluations")
candidates = get_all_candidates()
if candidates:
    st.table(candidates)
else:
    st.write("No candidate evaluations saved yet.")
