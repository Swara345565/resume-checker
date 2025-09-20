import fitz  # PyMuPDF for PDF
import docx2txt
import re

def extract_text_from_pdf(file_path):
    """
    Extracts raw text from a PDF file.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    """
    Extracts raw text from a DOCX file.
    """
    return docx2txt.process(file_path)

def parse_jd_skills(jd_text):
    """
    Extracts must-have and good-to-have skills from Job Description text.
    Returns a dictionary:
    {
        "must_have": [skill1, skill2, ...],
        "good_to_have": [skill1, skill2, ...]
    }
    """
    jd_text = jd_text.lower()

    # Simple regex-based extraction (you can improve later)
    must_have = []
    good_to_have = []

    # Look for sections labeled 'must have' or 'required'
    must_have_matches = re.findall(r"(must have|required|essential)[:\-]?\s*(.*)", jd_text)
    for match in must_have_matches:
        skills = match[1].split(",")
        must_have.extend([s.strip() for s in skills if s.strip()])

    # Look for sections labeled 'good to have' or 'optional'
    good_matches = re.findall(r"(good to have|optional|nice to have)[:\-]?\s*(.*)", jd_text)
    for match in good_matches:
        skills = match[1].split(",")
        good_to_have.extend([s.strip() for s in skills if s.strip()])

    return {
        "must_have": must_have,
        "good_to_have": good_to_have
    }

# Example usage:
if __name__ == "__main__":
    jd_file = "data/sample_jd.pdf"  # replace with your JD file path
    if jd_file.endswith(".pdf"):
        jd_text = extract_text_from_pdf(jd_file)
    else:
        jd_text = extract_text_from_docx(jd_file)

    skills = parse_jd_skills(jd_text)
    print("Must-Have Skills:", skills["must_have"])
    print("Good-to-Have Skills:", skills["good_to_have"])
