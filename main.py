from text_preprocessing import preprocess_jobstreet, preprocess_courses
import os
from text_representation import run_pipeline


# input dan output
JOB_PATH = 'data/jobstreet_listings.csv'
COURSE_PATH = 'data/Coursera_2021.csv'
OUTPUT_DIR = 'output'

#  memastikan output directory ada
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    #  1. preprocess job listings dan course data
    print(">> Preprocessing job listings...")
    job_df = preprocess_jobstreet(JOB_PATH)
    job_output_path = os.path.join(OUTPUT_DIR, 'preprocessed_jobs.csv')
    job_df.to_csv(job_output_path, index=False)
    print(f">> Saved preprocessed jobs to: {job_output_path}")

    print(">> Preprocessing course data...")
    course_df = preprocess_courses(COURSE_PATH)
    course_output_path = os.path.join(OUTPUT_DIR, 'preprocessed_courses.csv')
    course_df.to_csv(course_output_path, index=False)
    print(f">> Saved preprocessed courses to: {course_output_path}")

    #  2. vectorize data  dan 3. labeling & similarity

    print(">> Running similarity pipeline...")
    run_pipeline(
        job_path='output/preprocessed_jobs.csv',
        course_path='output/preprocessed_courses.csv',
        output_path=os.path.join(OUTPUT_DIR, 'recommendations.json')
    )

    print(">> Pipeline completed.")
    print(">> Recommendations saved to output/recommendations.json")

if __name__ == "__main__":
    main()
