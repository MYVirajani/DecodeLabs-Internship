import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_data
def load_and_build(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df['skills_original'] = df['skills']
    df['skills'] = df['skills'].str.lower().str.replace(',', ' ')
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df['skills'])
    return df, vectorizer, tfidf_matrix


def recommend(user_skills, df, vectorizer, tfidf_matrix, top_n=3):
    user_input = ' '.join([s.lower() for s in user_skills])
    user_vector = vectorizer.transform([user_input])
    scores = cosine_similarity(user_vector, tfidf_matrix)[0]
    result_df = pd.DataFrame({
        'job_role': df['job_role'].values,
        'skills_original': df['skills_original'].values,
        'similarity_score': scores
    })
    result_df = result_df.sort_values('similarity_score', ascending=False).head(top_n)
    return result_df



st.set_page_config(
    page_title="Tech Stack Recommender",
    layout="centered"
)

st.markdown("""
    <style>
        /* Background */
        .stApp {
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            color: white;
        }

        /* Hero */
        .hero {
            text-align: center;
            padding: 40px 20px 10px 20px;
        }
        .hero h1 {
            font-size: 2.8em;
            font-weight: 800;
            background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        .hero p {
            font-size: 1em;
            color: #94a3b8;
            margin-top: 0;
        }

        /* Section label */
        .section-label {
            font-size: 0.85em;
            font-weight: 700;
            color: #a78bfa;
            letter-spacing: 2px;
            text-transform: uppercase;
            margin-bottom: 8px;
            margin-top: 24px;
        }

        /* Result card */
        .card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(167, 139, 250, 0.3);
            border-radius: 16px;
            padding: 24px 28px;
            margin-bottom: 16px;
            backdrop-filter: blur(10px);
        }
        .card:hover {
            border-color: rgba(167, 139, 250, 0.8);
        }

        /* Rank badge */
        .rank-badge {
            display: inline-block;
            background: linear-gradient(135deg, #a78bfa, #60a5fa);
            color: white;
            font-weight: 700;
            font-size: 0.78em;
            padding: 4px 14px;
            border-radius: 20px;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }

        /* Job title */
        .job-title {
            font-size: 1.5em;
            font-weight: 700;
            color: #f1f5f9;
            margin: 6px 0;
        }

        /* Match score */
        .match-score {
            font-size: 1em;
            color: #34d399;
            font-weight: 600;
            margin: 8px 0 12px 0;
        }

        /* Skill tags */
        .skills-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .skill-tag {
            background: rgba(96, 165, 250, 0.12);
            border: 1px solid rgba(96, 165, 250, 0.35);
            color: #93c5fd;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.78em;
            font-weight: 500;
        }

        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
            border-radius: 10px;
        }
        .stProgress > div > div {
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
        }

        /* Button */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #a78bfa, #60a5fa);
            color: white;
            font-weight: 700;
            font-size: 1.05em;
            border: none;
            border-radius: 12px;
            padding: 14px;
            margin-top: 8px;
            letter-spacing: 0.5px;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: white;
        }

        /* Multiselect tags */
        span[data-baseweb="tag"] {
            background-color: #7c3aed !important;
            border-radius: 20px !important;
        }

        /* Divider */
        .divider {
            border: none;
            border-top: 1px solid rgba(255,255,255,0.08);
            margin: 28px 0;
        }

        /* Stats row */
        .stats-row {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin: 20px 0;
            text-align: center;
        }
        .stat-item {
            color: #94a3b8;
            font-size: 0.9em;
        }
        .stat-number {
            font-size: 1.8em;
            font-weight: 800;
            color: #a78bfa;
            display: block;
        }

        /* Footer */
        .footer {
            text-align: center;
            color: #475569;
            font-size: 0.82em;
            margin-top: 40px;
            padding-bottom: 30px;
        }

        /* Warning / error overrides */
        .stWarning, .stError {
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)

df, vectorizer, tfidf_matrix = load_and_build('raw_skills.csv')

all_skills = sorted(set(
    skill.strip()
    for skills in df['skills_original']
    for skill in skills.split(',')
))

st.markdown(f"""
    <div class="hero">
        <h1> Tech Stack Recommender</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

st.markdown('<div class="section-label">Step 1 — Select Your Skills</div>', unsafe_allow_html=True)

selected_skills = st.multiselect(
    label="",
    options=all_skills,
    placeholder="search and select your skills (minimum 3)..."
)

if selected_skills:
    st.markdown(f"**{len(selected_skills)} skills selected**")

st.markdown('<div class="section-label">Step 2 — Discover Your Path</div>', unsafe_allow_html=True)

clicked = st.button("Find Your Career Match")

if clicked:
    if len(selected_skills) < 3:
        st.warning("Please select at least 3 skills to get accurate recommendations.")
    else:
        with st.spinner("Analyzing your profile..."):
            results = recommend(selected_skills, df, vectorizer, tfidf_matrix)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Your Top Career Matches</div>', unsafe_allow_html=True)

        if results['similarity_score'].sum() == 0:
            st.error(" No matches found. Try selecting different skills or expand your dataset.")
        else:

            for rank, (_, row) in enumerate(results.iterrows(), start=1):
                match = round(row['similarity_score'] * 100, 2)

                skill_tags = ''.join([
                    f'<span class="skill-tag">{s.strip().upper()}</span>'
                    for s in row['skills_original'].split(',')
                ])

                st.markdown(f"""
                    <div class="card">
                        <div class="job-title">{row['job_role']}</div>
                        <div class="match-score">{match}% Compatibility</div>
                        <div class="skills-container">{skill_tags}</div>
                    </div>
                """, unsafe_allow_html=True)

                st.progress(match / 100)
                st.markdown("<div style='margin-bottom:8px'></div>", unsafe_allow_html=True)

