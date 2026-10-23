import pypdf
import docx
import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from the .env file
load_dotenv()

def extract_text_from_pdf(uploaded_file):
    pdf = pypdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(uploaded_file):
    doc = docx.Document(uploaded_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

# Streamlit User Interface
st.title("AI Resume Analyzer")

# 1. Job Description text area
job_description = st.text_area("Paste the Job Description here:")

# 2. File uploader for resume
uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])

# 3. Submit button
if st.button("Analyze Resume"):
    if uploaded_file is not None and job_description:
        # Check file type and extract text
        if uploaded_file.name.endswith(".pdf"):
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.name.endswith(".docx"):
            resume_text = extract_text_from_docx(uploaded_file)
        
        with st.spinner("Analyzing resume with Gemini..."):
            try:
                # Initialize Gemini client (it automatically finds GEMINI_API_KEY from your .env file)
                client = genai.Client()
                
                # Construct prompt for the model
                prompt = f"""
                You are an expert HR recruiter and ATS (Applicant Tracking System) analyzer.
                Please analyze the following resume against the given job description.

                Job Description:
                {job_description}

                Resume Text:
                {resume_text}

                Please provide a detailed report containing:
                1. **Match Score**: A percentage score estimating how well the resume matches the job description.
                2. **Matching Skills**: List the skills found in both the resume and the job description.
                3. **Missing Keywords/Skills**: Identify important skills or keywords present in the job description that are missing from the resume.
                4. **Areas for Improvement**: Actionable recommendations on how the candidate can improve their resume for this specific role.
                """

                # Call Gemini API using the updated model name
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )

                st.success("Analysis Complete!")
                st.markdown("### Analysis Report")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please make sure you have pasted the job description and uploaded a resume.")