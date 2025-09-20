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
        # docx2txt requires a path, so write temp file
        temp_path = "temp_jd.docx"
        with open(temp_path, "wb") as f:
            f.write(file.read())
        return docx2txt.process(temp_path)

    else:
        raise ValueError("Unsupported file type")

def parse_jd(file):
    """
    Parse JD UploadedFile and return structured dict:
    {
        "role": str,
        "must_have_skills": [...],
        "good_to_have_skills": [...],
        "full_text": str
    }
    """
    jd_text = extract_text(file)
    jd_text_lower = jd_text.lower()

    # Role title: first line or first non-empty line
    lines = [line.strip() for line in jd_text.split("\n") if line.strip()]
    role = lines[0] if lines else "Unknown Role"

    # Must-have skills
    must_have = []
    for match in re.findall(r"(must have|required|essential)[:\-]?\s*(.*)", jd_text_lower):
        skills = [s.strip().capitalize() for s in match[1].split(",") if s.strip()]
        must_have.extend(skills)

    # Good-to-have skills
    good_to_have = []
    for match in re.findall(r"(good to have|optional|nice to have)[:\-]?\s*(.*)", jd_text_lower):
        skills = [s.strip().capitalize() for s in match[1].split(",") if s.strip()]
        good_to_have.extend(skills)

    return {
        "role": role,
        "must_have_skills": must_have,
        "good_to_have_skills": good_to_have,
        "full_text": jd_text
    }

# Example usage
if __name__ == "__main__":
    import streamlit as st
    jd_file = st.file_uploader("Upload JD", type=["pdf", "docx"])
    if jd_file:
        jd_parsed = parse_jd(jd_file)
        st.write(jd_parsed)
