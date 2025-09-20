import pdfplumber
import docx2txt
import re

def extract_text(file):
    """
    Extract text from Streamlit UploadedFile (PDF or DOCX)
    """
    # PDF
    if file.type == "application/pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    # DOCX
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        temp_path = "temp_resume.docx"
        with open(temp_path, "wb") as f:
            f.write(file.read())
        return docx2txt.process(temp_path)

    else:
        raise ValueError("Unsupported file type")

def parse_resume(file):
    """
    Parse Resume UploadedFile and return structured dict:
    {
        "skills": [...],
        "education": [...],
        "projects": [...],
        "experience": [...],
        "full_text": str
    }
    """
    text = extract_text(file)
    text_lower = text.lower()

    # Skills (look for lines with 'skills' or 'technologies')
    skills = []
    skills_matches = re.findall(r"(skills|technologies|tools)[:\s]*(.*)", text_lower)
    for match in skills_matches:
        skills += [s.strip().capitalize() for s in re.split(r",|;|\n", match[1]) if s.strip()]

    # Education (look for keywords)
    education = list(set(re.findall(r"(b\.tech|b\.sc|m\.tech|m\.sc|mba|phd|degree|graduation|college)", text_lower)))

    # Projects (lines containing 'project')
    projects = [line.strip() for line in text.split("\n") if "project" in line.lower()]

    # Experience (lines with 'experience' or 'worked at')
    experience = [line.strip() for line in text.split("\n") if "experience" in line.lower() or "worked at" in line.lower()]

    return {
        "skills": skills,
        "education": education,
        "projects": projects,
        "experience": experience,
        "full_text": text
    }

# Example usage
if __name__ == "__main__":
    import streamlit as st
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])
    if resume_file:
        resume_parsed = parse_resume(resume_file)
        st.write(resume_parsed)
