# automated_short_answer_grading

Student_app = https://automaticgradingsystemwebapp-lwki3pekkq-uc.a.run.app
Admin_app(Professor_app) = https://automaticgradingsystemadminapp-lwki3pekkq-uc.a.run.app/

We utilized Google Cloud Storage, Cloud Functions, and Google Cloud Run to deploy our code.

Note that in the Admin application, the Professor is required to upload two CSV files: one containing the questions and their original answers, and the other containing the student IDs and passwords for authentication. Both of these files are located in the "files_to_upload_by_professor" folder. If the Professor wishes to add, edit, or delete any questions/answers or student credentials, they can do so directly on those CSV files and upload again on Admin_app.

Admin panel
-------------
deployment link:- https://automaticgradingsystemadminapp-lwki3pekkq-uc.a.run.app/

1. To take the exam, prof can have csv file of questions and original answers, to provide access to students he also should have student_credentials file, (like we already have)

these two apis we created to do so.
- store_prof_questions_answers_File_to_google_cloud_storage
  https://us-central1-automaticgradingsystem.cloudfunctions.net/upload_prof_ques_ans_file

-store_student_credentials_File_to_google_cloud_storage 
  https://us-central1-automaticgradingsystem.cloudfunctions.net/upload_student_credentials_file

2. then prof can upload both of the file using admin pannel url
    so we take that file and store them into the google cloud storage.

User Panel
--------------
deployment link:- https://automaticgradingsystemwebapp-lwki3pekkq-uc.a.run.app

1. students will have exam links in which they'll have questions and space for answers and also they have to login to appear in exam

2. to make this kinda UI, we have used streamlit, 

3. Prof already uploaded students credentials file, having students id and password, so only those students can only appear on exam. for authentication, we read that prof file from google cloud storage, matchup the studentid and password in that file and allowed only authenticated students to show questons and answers.
student authentication api:- https://us-central1-automaticgradingsystem.cloudfunctions.net/fetch_student_credentials_data

4. questons are dynamic, prof can update or add questions and original answers to csv file and upload from admin side.
api to show questions form:- https://us-central1-automaticgradingsystem.cloudfunctions.net/fetch_prof_questions_answer_data

5. now students can write the test
6. after finishing there is submit button, so we take all the answers of students and ready original answers of prof form the uploaded csv file from google cloud storage and apply bert model on that to calculate the score.
api to calculate score:- https://us-central1-automaticgradingsystem.cloudfunctions.net/calculate_score

7. after that we are showing final grade back to the UI.
