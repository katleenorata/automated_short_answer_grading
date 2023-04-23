from google.cloud import storage
import csv
import json  

def fetch_student_credentials_data(request):
    # create a client object for your GCS project
    client = storage.Client()

    # specify the name of your GCS bucket and the path to your CSV file
    bucket_name = 'prof_ques_answer_file'
    file_name = 'file_student_credentials.csv'
    blob_name = f'{file_name}'

    # get a reference to the GCS file as a blob object
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # # read the CSV data from the blob into a pandas dataframe
    data = blob.download_as_text()
    # df = pd.read_csv(data)
    # parse the CSV data into a list of dictionaries
    csv_reader = csv.reader(data.splitlines())
    data = [row for row in csv_reader]
    
    # return the data as a JSON object
    return json.dumps(data)



    
    
