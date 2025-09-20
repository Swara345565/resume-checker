import pdfplumber
import docx2txt

def extract_text_from_pdf(file_path):
    """Extract text from a PDF using pdfplumber"""
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file_path):
    """Extract text from a DOCX file"""
    return docx2txt.process(file_path)

# Example usage
if __name__ == "__main__":
    pdf_file = "/data/Resumes/resume - 1.pdf"
    docx_file = "/data/Resumes/SwaraliPatil_GenAI_Consultant_Resume.docx"

    print("PDF Resume Text:\n", extract_text_from_pdf(pdf_file))
    print("\nDOCX Resume Text:\n", extract_text_from_docx(docx_file))
