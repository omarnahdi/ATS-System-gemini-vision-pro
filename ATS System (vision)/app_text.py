import google.generativeai as genai 
import os
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import PyPDF2 as pdf
import pdf2image 

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
st.set_page_config(page_title="Application Tracking System", page_icon="🤖")

def gemini_response(user_input):
    model = genai.GenerativeModel('gemini-pro')
    
    response = model.generate_content(user_input)
    return response.text

def pdf_reader(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
        
    return text

def pdf_converter(uploaded_file):
    images = pdf2image.convert_from_bytes(uploaded_file.getvalue())
    return images

st.title("Application Tracking System",anchor=False)
para = """Welcome to the Application Tracking System. Please upload a PDF file to get started. 
        This application is completely created by **Omar Nahdi**.
            
Next steps: 
- Upload your resume(in PDF format).
- Paste the job description.
- Select your input from the given options.
"""

st.write(para)
JD = st.text_area("Job Description", key="job_description",placeholder="Paste the job description here",height=200)

uploaded_file = st.file_uploader("Upload your resume in PDF format", type=["pdf"])
if uploaded_file is not None:
    st.success("File uploaded successfully", icon="✅")
    st.write("File name:", uploaded_file.name)
    img = pdf_converter(uploaded_file)
    text = pdf_reader(uploaded_file)
    st.image(img[:])
    
submit1 = st.button("Tell me about the resume")


input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst,
AI , ML, big data engineer, etc. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy

Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.

Mention candidate's achievemnets/projects/milestones if mentioned in the resume.

resume:{text}
description:{jd}

I want the response in this structure
JD Match: %

MissingKeywords:[
    
    ]
    
    
Profile Summary:


"""

if submit1:
    if uploaded_file is not None:
        response = gemini_response(input_prompt)
        st.write(response)
    else:
        st.error("Please upload a PDF file", icon="🚨")
