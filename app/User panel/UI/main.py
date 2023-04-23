# from calculating_grade import calculate_score
import streamlit as st
import requests
import json
import time
import pandas as pd

flag = True

# Define the URL of the API that will process the form data
API_URL_PROF_QUES_ANS_DATA = "https://us-central1-automaticgradingsystem.cloudfunctions.net/fetch_prof_questions_answer_data"
API_URL_FETCH_STUDENT_CREDENTIALS_DATA = 'https://us-central1-automaticgradingsystem.cloudfunctions.net/fetch_student_credentials_data'

# Define the questions and correct answers
questions = []

@st.cache_data
def fetch_prof_ques_ans_data():
    response = requests.post(API_URL_PROF_QUES_ANS_DATA)

    # Convert the CSV data to a list of lists
    csv_list = response.content
    csv_list = csv_list.decode()
    csv_list = json.loads(csv_list)

    # Create a list of dictionaries for each question
    questions_list = []
    for i in range(1,len(csv_list)):
        question_dict = {}
        question_dict['question_id'] = csv_list[i][0]
        question_dict['Questions'] = csv_list[i][1]
        question_dict['Answers'] = csv_list[i][2]
        questions_list.append(question_dict)

    return questions_list

# Create the Streamlit app

# Define a function to check if the user ID and password are valid
def authenticate_user(idd, password):
    response = requests.post(API_URL_FETCH_STUDENT_CREDENTIALS_DATA)
    time.sleep(2)
    # Convert the CSV data to a list of lists
    csv_list = response.content
    csv_list = csv_list.decode()
    csv_list = json.loads(csv_list)

    print(csv_list)

    df = pd.DataFrame(csv_list[1:], columns=['ID','Password'])  # Load the user data from a list of lists
    for index, row in df.iterrows():
        if row['ID'] == idd and row['Password'] == password:
            return True
    return False

def app():
    st.title("Student Login")
    st.write("Please enter your ID and password to login:")

    # Add text input fields for the user ID and password
    user_id = st.text_input("ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        with st.spinner('Authenticating...'):
            if authenticate_user(user_id, password):
                st.success("Login successful!")
                # Open the next page in Streamlit
                next_page(user_id)
                st.session_state.load_state = False
                st.session_state.key = False
            else:
                st.error("Invalid ID or password. Please try again.")

    if(st.session_state.load_state == False and st.session_state.key == True):
        next_page(user_id)
    
    st.session_state.key = True
    
   

def next_page(user_id):
    
    # Fetch the data from prof_ques_ans_file and store in the questions list to show UI.
    global questions 
    questions= fetch_prof_ques_ans_data()

    st.title("Welcome, " + user_id + "!")
    st.title("Short Questions Answers")
    
    # Create a multiselect widget to allow users to choose which questions they want to answer
    selected_questions = st.multiselect("Select questions to answer", [q["question_id"] for q in questions], default=None)
    
    # Filter questions based on the user's selection
    filtered_questions = [q for q in questions if q["question_id"] in selected_questions] if selected_questions else questions
    
    # Display the form with questions and space for answers
    user_answers = {}
    for i, question in enumerate(filtered_questions):
        st.subheader(f"Question {question['question_id']}")
        st.write(question["Questions"])
        user_answers[question['question_id']] = st.text_area(f"Your answer for Question {i+1}:", key=question['question_id'])
    
    # Add a submit button to the form
    if st.button("Submit"):
        # Append user's answers to questions
        for question in questions:
            if question['question_id'] in user_answers.keys():
                question['student_answers'] = user_answers[question['question_id']]
            else:
                question['student_answers'] = ""
        
        json_data = {"df_to_calculate_score": questions}
        json_string = json.dumps(json_data)

        # Send the user's answers to the API for processing
        with st.spinner('Calculating your score...'):
            response = requests.post("https://us-central1-automaticgradingsystem.cloudfunctions.net/calculate_score", json=json_string)
        
        # Parse the response data
        result = json.loads(response.text)
        
        # Display the result of the processing, including the grade
        st.write("Result:")
        with st.spinner('Loading result...'):
            time.sleep(2) # Simulating a delay for the result
            st.subheader(f"Grade: {result['grade']}")

            # Display the correct answers and student answers in a table
            correct_answers = {}
            for i, answer in enumerate(questions):
                correct_answers[f'{i+1}'] = answer['Answers']
            student_answers = {}
            for i, question in enumerate(questions):
                student_answers[f'{i+1}'] = question['student_answers']
            result = {'Question': [], 'Correct Answer': [], 'Student Answer': []}
            for i in range(1, len(questions)+1):
                result['Question'].append(f"{i}. {questions[i-1]['Questions']}")
                result['Correct Answer'].append(correct_answers[f'{i}'])
                result['Student Answer'].append(student_answers[f'{i}'])
            st.write("Answers:")
            st.table(result)
            
st.set_page_config(page_title="Quiz", page_icon=":memo:", layout="wide")

def main():
    if "load_state" not in st.session_state:
        st.session_state.load_state = True
    if "key" not in st.session_state:
        st.session_state.key = True

    # if(st.session_state.load_state):
    app()
    

if __name__ == '__main__':
    main()

