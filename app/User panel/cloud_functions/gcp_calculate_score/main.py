import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import json
import requests
import numpy as np

model_id = "sentence-transformers/all-MiniLM-L6-v2"
hf_token = "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"

api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

# def load_transformer_model():
#     # client = storage.Client()
#     # bucket_name = 'prof_ques_answer_file'
#     # model_folder_name = 'transformer_model'
#     # bucket = client.get_bucket(bucket_name)
#     # blob = bucket.blob(model_folder_name + '/config.json')
#     # model_config = blob.download_as_string()
#     # blob = bucket.blob(model_folder_name + '/pytorch_model.bin')
#     # model_weights = blob.download_as_bytes()
#     # model = SentenceTransformer(None, None, model_config=model_config, model_weights=model_weights)
#     model_path = "transformer_model/"
#     model = SentenceTransformer(model_path)
#     return model

def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options":{"wait_for_model":True}})
    return response.json()

def calculate_score(request):
    request_dict = json.loads(request.json)
    df_to_calculate_score = request_dict.get('df_to_calculate_score')
    df = pd.DataFrame(df_to_calculate_score)

    student_answers = df['student_answers'].tolist()
    student_answers_embeddings = query(student_answers)
    df['student_answers_embeddings'] = student_answers_embeddings

    Answers = df['Answers'].tolist()
    answers_embeddings = query(Answers)
    df['answers_embeddings'] = answers_embeddings

    # # calculate word embeddings
    # df['student_answers_embeddings'] = df['student_answers'].apply(lambda x : model.encode([x]))
    # df['answers_embeddings'] = df['Answers'].apply(lambda x : model.encode([x]))

    # convert the embeddings from list to numpy array
    student_answers_embeddings = np.array(df['student_answers_embeddings'].tolist())
    answers_embeddings = np.array(df['answers_embeddings'].tolist())

    # calculate cosine similarity between student_answers_embeddings and answers_embeddings
    similarity_scores = cosine_similarity(student_answers_embeddings, answers_embeddings)

    # add a new column named similarity_score to the dataframe
    df['Bert_similarity_score'] = similarity_scores.diagonal()

    # #Apply cosine similarity on word embeddings
    # df['Bert_similarity_score'] = df.apply(lambda row: cosine_similarity(row['student_answers_embeddings'],row['answers_embeddings']),axis=1)
    # df['Bert_similarity_score'] = df['Bert_similarity_score'].apply(lambda x: x[0][0])
    final_grade = ""
    score = (df['Bert_similarity_score'].mean())*100
    if(score>0 and score<=20):
        final_grade="E"
    elif(score>20 and score<=40):
        final_grade="D"
    elif(score>40 and score<=60):
        final_grade="C"
    elif(score>60 and score<=80):
        final_grade="B"
    else:
        final_grade="A"

    return {
        "score": score,
        "grade":final_grade
    }

