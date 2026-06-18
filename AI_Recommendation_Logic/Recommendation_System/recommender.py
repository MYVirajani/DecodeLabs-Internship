import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_data(filepath):
    df = pd.read_csv(filepath)
    df['skills'] = df['skills'].str.lower()
    return df


def build_tfidf_matrix(df):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['skills'])
    return vectorizer, tfidf_matrix


def score_user_profile(user_skills, vectorizer, tfidf_matrix):
    user_input = ' '.join([skill.lower() for skill in user_skills])

    user_vector = vectorizer.transform([user_input])
    
    scores = cosine_similarity(user_vector, tfidf_matrix)
    return scores[0]  


def get_top_recommendations(df, scores, top_n=3):
    df = df.copy()
    df['similarity_score'] = scores
    
    results = df.sort_values('similarity_score', ascending=False).head(top_n)
    return results[['job_role', 'similarity_score']]


def main():
    print("=" * 50)
    print(" Tech Stack Recommender")
    print("=" * 50)
    
    df = load_data('raw_skills.csv')
    vectorizer, tfidf_matrix = build_tfidf_matrix(df)
    
    print("\nEnter your skills one by one.")
    print("Type 'done' when finished (minimum 3 skills).\n")
    
    user_skills = []
    while True:
        skill = input(f"Skill {len(user_skills) + 1}: ").strip()
        if skill.lower() == 'done':
            if len(user_skills) < 3:
                print("Please enter at least 3 skills.")
            else:
                break
        elif skill:
            user_skills.append(skill)
    
    print(f"\nYour skills: {user_skills}")
    
    scores = score_user_profile(user_skills, vectorizer, tfidf_matrix)
    recommendations = get_top_recommendations(df, scores, top_n=3)
    
    print("\n" + "=" * 50)
    print("   Top 3 Recommended Career Paths")
    print("=" * 50)
    
    for rank, (_, row) in enumerate(recommendations.iterrows(), start=1):
        match_percent = round(row['similarity_score'] * 100, 2)
        print(f"\n#{rank}  {row['job_role']}")
        print(f"    Match Score: {match_percent}%")
    
    if recommendations['similarity_score'].sum() == 0:
        print("\n[WARNING] No matches found. Your skills may not exist")
        print("in the dataset vocabulary. Check your spelling or expand")
        print("the dataset with more job roles and skills.")

if __name__ == "__main__":
    main()