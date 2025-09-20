import streamlit as st
from backend.parse_resume import extract_text_from_pdf, extract_text_from_docx
from backend.scoring import score_resume

st.title("📄 Automated Resume Relevance Checker")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
resume_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=["pdf", "docx"])

must_have_skills = st.text_area("Enter must-have skills (comma-separated)").split(",")

if jd_file and resume_file:
    # Parse JD
    if jd_file.type == "application/pdf":
        jd_text = extract_text_from_pdf(jd_file)
    else:
        jd_text = extract_text_from_docx(jd_file)

    # Parse Resume
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_text = extract_text_from_docx(resume_file)

    # Score
    score, verdict, missing = score_resume(resume_text, jd_text, must_have_skills)

    st.subheader("Results")
    st.write(f"**Relevance Score:** {score:.2f}")
    st.write(f"**Verdict:** {verdict}")
    st.write(f"**Missing Skills:** {', '.join(missing) if missing else 'None'}")
