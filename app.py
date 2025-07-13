import base64
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import io
from PIL import Image
import pdf2image # type: ignore
import google.generativeai as genai # type: ignore


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))    
def get_gemini_response(input,pdf_content,prompt):
    # model = genai.GenerativeModel("gemini-1.5-pro")
    # or
    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content([input,pdf_content[0],prompt])
    return response.text



def input_pdf_setup(uploaded_file):

    if uploaded_file is not None:
        # convert the pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())


        first_page= images[0]

        # convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr=img_byte_arr.getvalue()


        pdf_parts=[
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode(),   #encode to base 64
                
            }
        ]


        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded or file is not a PDF.")
    

# streamlit app
st.set_page_config(page_title="ATS Tracker")
st.header("ATS Tracker")
input_text = st.text_area("Job Description", key="input")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])


if uploaded_file is not None:
    st.write("PDF file uploaded successfully.")

submit1= st.button("Tell me about the resume")
#submit2= st.button("How can I improve my skills?")
submit3= st.button("Percentage Match")



input_prompt1 = "Analyze the resume and provide insights on how well it matches the job description. " \
"Provide a detailed analysis of the skills, experience, and qualifications in the resume in relation to the job description."

input_prompt2 = " You are an experienced HR with tech experience in the field of any one job role from data science or full stack web development " \
"or big data engineering or devops or data analyst " \
"your task is to review the provided resume against the job description for these profiles. Please share your professional " \
"evaluation on whether the candidates profile aligns with the job" \
" description highlight the strengths and weaknesses of the applicant in relation to the specified job role"

input_prompt3 = " You are an skilled ATS application tracking system scanner whether deep understanding of any one job role data science " \
"or full stack web development or big data engineering or devops or data analyst and ATS functionality your task is to evaluate the resume " \
"against the provided job description give me the percentage" \
" match with the job disruption first the output should come as percentage and then keywords missing from the resume " \
"in relation to the job description."

if submit1:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("Resume Analysis")
        st.write(response)
    else:
        st.write("Please upload a PDF resume.")


elif submit3:
    if uploaded_file is not None:
        pdf_content= input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3,pdf_content,input_text)
        st.subheader("Percentage Match")
        st.write(response)
    else:
        st.write("Please upload a PDF resume.")
        

