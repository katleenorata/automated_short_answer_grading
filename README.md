# automated_short_answer_grading

Student_app = https://automaticgradingsystemwebapp-lwki3pekkq-uc.a.run.app
Admin_app(Professor_app) = https://automaticgradingsystemadminapp-lwki3pekkq-uc.a.run.app/

We utilized Google Cloud Storage, Cloud Functions, and Google Cloud Run to deploy our code.

Note that in the Admin application, the Professor is required to upload two CSV files: one containing the questions and their original answers, and the other containing the student IDs and passwords for authentication. Both of these files are located in the "files_to_upload_by_professor" folder. If the Professor wishes to add, edit, or delete any questions/answers or student credentials, they can do so directly on those CSV files and upload again on Admin_app.
