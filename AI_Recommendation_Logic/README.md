#  Tech Stack Recommender



---

## 📌 Overview

**Tech Stack Recommender** is a content-based AI recommendation system that maps a user's skills to the most relevant career paths using **TF-IDF vectorization** and **Cosine Similarity**.
Instead of random suggestions, the system performs **mathematical pattern matching** — converting raw skill inputs into weighted vectors and computing angular similarity against a dataset of job roles.

---

## 🎯 Project Goals

- Understand the shift from passive classification to active prediction
- Implement a full **Input → Process → Output (IPO)** recommendation pipeline
- Apply **TF-IDF weighting** to penalize generic terms and reward specific ones
- Use **Cosine Similarity** as a magnitude-invariant similarity metric
- Build a functional, interactive web UI using **Streamlit**

---

## 🧠 How It Works

The system follows a strict **4-step ranking pipeline**:

```
User Skills Input
      │
      ▼
① INGESTION    — Capture user skill selections (minimum 3)
      │
      ▼
② SCORING      — TF-IDF vectorization + Cosine Similarity calculation
      │
      ▼
③ SORTING      — Rank all job roles by similarity score (descending)
      │
      ▼
④ FILTERING    — Return Top 3 highest-scoring career matches
```

### Why TF-IDF?
TF-IDF assigns higher weight to **specific, rare skills** (e.g. `Kubernetes`) and penalizes **generic, common terms** (e.g. `software`). This ensures unique skills have a greater impact on matching accuracy.

### Why Cosine Similarity?
Unlike Euclidean distance, Cosine Similarity is **invariant to vector magnitude** — it measures the angular alignment between two vectors. This means a user with 3 skills and a job role with 10 skills are compared fairly based on **direction of interest**, not size.

```
cos(θ) = (A · B) / (‖A‖ × ‖B‖)

Score 1  → Perfect match (identical orientation)
Score 0  → No common characteristics
```

---

## 🗂️ Project Structure

```
AI_Recommendation_Logic/
│
├── app.py               ← Streamlit web application
├── recommender.py       ← Terminal-based version
├── raw_skills.csv       ← Job roles dataset
├── requirements.txt     ← Python dependencies
├── .gitignore           ← Excludes venv and cache files
└── README.md            ← Project documentation
```

---

## 📊 Dataset — `raw_skills.csv`

The dataset treats **job roles as items** in the recommendation engine. Each row contains a job role and its associated skills as a comma-separated string.

| job_role | skills |
|---|---|
| Data Scientist | Python, SQL, Machine Learning, Data Analysis, Statistics, Deep Learning |
| DevOps Engineer | AWS, Docker, Kubernetes, CI/CD, Linux, Git, Automation, Cloud |
| ML Engineer | Python, TensorFlow, PyTorch, Deep Learning, Neural Networks, Optimization |
| AI Engineer | Python, NLP, Computer Vision, LLMs, RAG Pipelines, Deep Learning, TensorFlow |
| ... | ... |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MYVirajani/DecodeLabs-Internship.git
cd AI_Recommendation_Logic
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
```bash
# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

### Streamlit Web App
```bash
streamlit run app.py
```
Opens automatically at `http://localhost:8501`

### Terminal Version
```bash
python recommender.py
```

---

## 🖥️ Usage

1. Open the web app in your browser
2. **Step 1** — Search and select your skills from the dropdown (minimum 3)
3. **Step 2** — Click **"Find Your Career Match"**
4. View your **Top 3 recommended career paths** with compatibility scores and skill tags

---

## 📦 Requirements

```
pandas
numpy
scikit-learn
streamlit
```

Install all at once:
```bash
pip install pandas numpy scikit-learn streamlit
```

Or use the requirements file:
```bash
pip install -r requirements.txt
```

---

## 🔑 Key Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Content-Based Filtering | Matches user profile to item attributes without needing other users' data |
| TF-IDF Vectorization | `TfidfVectorizer()` from scikit-learn |
| Cosine Similarity | `cosine_similarity()` from scikit-learn |
| Shared Vocabulary Space | `vectorizer.transform()` maps user input to same space as dataset |
| Cold Start Handling | Zero-score detection with error message |
| Top-N Filtering | `.sort_values().head(3)` |
| IPO Architecture | Input (skills) → Process (similarity) → Output (ranked roles) |


