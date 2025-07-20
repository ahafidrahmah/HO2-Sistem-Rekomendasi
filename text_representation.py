import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
import os

# model Sentence-BERT
model = SentenceTransformer('all-MiniLM-L6-v2')

def load_data(job_path, course_path):
    job_df = pd.read_csv(job_path)
    course_df = pd.read_csv(course_path)

    # validasi kolom
    assert 'cleaned_text' in job_df.columns
    assert 'cleaned_text' in course_df.columns
    assert 'Course Name' in course_df.columns

    return job_df, course_df

def compute_embeddings(text_list):
    return model.encode(text_list, convert_to_tensor=True)

def map_similarity(job_df, course_df, top_k=3):
    job_embeddings = compute_embeddings(job_df['cleaned_text'].tolist())
    course_embeddings = compute_embeddings(course_df['cleaned_text'].tolist())

    all_results = []

    print(">> Calculating similarities...")
    for i, job_row in job_df.iterrows():
        job_text = job_row['cleaned_text']
        job_title = job_row.get('job_title', f"Job {i+1}")
        job_category = job_row.get('category', 'Unknown')

        sim_scores = util.cos_sim(job_embeddings[i], course_embeddings)[0]
        top_indices = torch.topk(sim_scores, k=top_k).indices.cpu().numpy()

        recommended_courses = [
            {
                'course_name': course_df.loc[idx, 'Course Name'],
                'score': float(sim_scores[idx])
            }
            for idx in top_indices
        ]

        all_results.append({
            'job_title': job_title,
            'job_category': job_category,
            'recommended_courses': recommended_courses
        })

    return all_results

def save_recommendations(results, output_path='output/recommendations.json'):
    import json
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f">> Saved recommendations to {output_path}")

def run_pipeline(job_path='output/preprocessed_jobs.csv',
                 course_path='output/preprocessed_courses.csv',
                 output_path='output/recommendations.json'):
    job_df, course_df = load_data(job_path, course_path)
    recommendations = map_similarity(job_df, course_df, top_k=3)
    save_recommendations(recommendations, output_path)

if __name__ == '__main__':
    run_pipeline()
