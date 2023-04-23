from google.cloud import storage

BUCKET_NAME = 'prof_ques_answer_file'

# Create a function to upload the CSV file to Google Cloud Storage
def upload_prof_ques_ans_file(request):
    csv_file = request.files["file"]
    # Set up the Google Cloud Storage client
    client = storage.Client()
    bucket = client.get_bucket(BUCKET_NAME) # Replace with your bucket name
    
    # Upload the file to the bucket
    blob = bucket.blob(f'{csv_file.name}.csv')
    blob.upload_from_file(csv_file)
    
    # Get the URL of the uploaded file
    url = f"https://storage.googleapis.com/{bucket.name}/{blob.name}"
    
    return url