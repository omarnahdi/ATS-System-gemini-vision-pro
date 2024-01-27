import google.generativeai as genai 
import os
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
import pdf2image

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
st.set_page_config(page_title="Application Tracking System", page_icon="🤖")

def gemini_response(user_input,JD,img):
    model = genai.GenerativeModel('gemini-pro-vision')
    
    response = model.generate_content([user_input,JD,img[0]])
    return response.text

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
    
submit1 = st.button("Tell me about the resume")

submit2 = st.button("Percentage match")

input_prompt1 = """
 You are an experienced HR with technical experience in the field of any one job role data science, Artificial Intelligence, Machine Learning, Full stack web development, Big Data Engineering, DevOps, Data Analyst.
 your task is to review the provided resume against the job description for this profiles. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role data science, Artificial Intelligence, Machine Learning, Full stack web development, Big Data Engineering, DevOps, Data Analyst and deep ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


if submit1:
    if uploaded_file is not None:
        response = gemini_response(input_prompt1,JD,img)
        st.write(response)
    else:
        st.error("Please upload a PDF file", icon="🚨")

elif submit2:
    if uploaded_file is not None:
        response = gemini_response(input_prompt2,JD,img)
        st.write(response)
    else:
        st.error("Please upload a PDF file", icon="🚨")

 