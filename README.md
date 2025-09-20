# 📄 AI-Powered Resume Relevance Checker

## 💡 Overview
Recruiters often spend countless hours manually reviewing resumes, leading to delays, inconsistencies, and reduced focus on student guidance. This project provides an **automated solution** to evaluate resumes against job descriptions, generate relevance scores, and deliver actionable feedback to students—all through a user-friendly web interface.

---

## 🎯 Goals
- Quickly evaluate resumes at scale
- Assign a **Relevance Score (0–100)** for each resume
- Identify missing skills, certifications, or key projects
- Provide a **fit assessment**: High / Medium / Low
- Suggest personalized improvements for students
- Store evaluations in a searchable dashboard for placement teams

---

## 🛠️ Technology Stack

**Backend & AI**
- Python 3.10+  
- `pdfplumber` / `docx2txt` → Resume and Job Description text extraction  
- `RapidFuzz` / `scikit-learn` → Hard skill matching  
- `Sentence-Transformers` → Semantic similarity calculations  
- SQLite → Database for storing candidate data  

**Frontend**
- Streamlit → Interactive web interface for uploads and dashboards  

**Deployment**
- Streamlit Cloud 

---

## 🔄 Workflow

1. **Upload Job Description (JD)** – Placement team submits JD files (PDF/DOCX)  
2. **Upload Resumes** – Students submit their resumes (PDF/DOCX)  
3. **Text Extraction** – Clean and standardize text from uploaded files  
4. **Relevance Evaluation**  
   - **Hard Match:** Exact keyword and skill checks  
   - **Soft Match:** Semantic similarity using embeddings  
   - **Weighted Scoring:** Combine both for final relevance score  
5. **Result Generation**  
   - Relevance Score  
   - Missing skills or projects  
   - Suitability Verdict (High / Medium / Low)  
   - Suggested improvements for students  
6. **Dashboard Access** – Placement team can view, filter, and search candidate evaluations

---

## ⚡ Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/Swara345565/resume-checker.git
cd resume-checker

2. Set Up Environment
conda create -n resume-checker python=3.10 -y
conda activate resume-checker

3. Install Dependencies
pip install -r requirements.txt

4. Launch the App
streamlit run app.py

📽️ Demo Video



🌐 Live Web App

https://team03toptechnerds.streamlit.app/

👥 Team Members

Team Name: Top TechNerds

Name	                      Email	                  Contact
Swarali Dhanaji Patil	swaralip35@gmail.com         9869715575
Mitali Sonawale	      mitalisonavale78@gmail.com     9970658279
Gauravi Ubhare	     gauraviubhare2908@gmail.com     8591742566

🔮 Future Enhancements

Automatic parsing of JD for must-have vs good-to-have skills

Advanced LLM-powered feedback generation

Integration with placement portals for seamless student uploads

Multilingual resume support

📜 Declaration

We declare that this project is developed entirely by our team for the Innomatics Hackathon 2025. All tools, references, and libraries are properly acknowledged.
