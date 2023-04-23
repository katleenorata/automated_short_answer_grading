import streamlit as st
import requests

API_URL_PROF_QUES_ANS_FILE = 'https://us-central1-automaticgradingsystem.cloudfunctions.net/upload_prof_ques_ans_file'
API_URl_FOR_STUDENT_CREDENTIALS = 'https://us-central1-automaticgradingsystem.cloudfunctions.net/upload_student_credentials_file'

# Create the Streamlit app
st.title("Upload a CSV file to Google Cloud Storage")

# Add a file uploader to the app
file = st.file_uploader("Upload a CSV file of Questions and Answers")

# If a file was uploaded
if file:
    # Upload the file to Google Cloud Storage
    response = requests.post(API_URL_PROF_QUES_ANS_FILE, files={"file": file})
    
    # Display the URL of the uploaded file
    st.success(f"File uploaded to Server {response}")

# Add a file uploader to the app
file = st.file_uploader("Upload a CSV file of Student Credentials")

# If a file was uploaded
if file:
    # Upload the file to Google Cloud Storage
    response = requests.post(API_URl_FOR_STUDENT_CREDENTIALS, files={"file": file})
    
    # Display the URL of the uploaded file
    st.success(f"File uploaded to Server {response}")


