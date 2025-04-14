from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer('all-MiniLM-L6-v2')

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def calculate_fit_score(resume_text, job_description):
    resume_clean = clean_text(resume_text)
    job_clean = clean_text(job_description)

    # TF-IDF Score
    vectorizer = TfidfVectorizer(stop_words='english', max_features=500)
    tfidf_matrix = vectorizer.fit_transform([resume_clean, job_clean])
    tfidf_similarity = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    # Semantic Score
    resume_emb = model.encode(resume_clean)
    job_emb = model.encode(job_clean)
    semantic_similarity = util.cos_sim(resume_emb, job_emb).item()

    # Combined Score (Weighted average)
    combined_score = round((0.4 * tfidf_similarity + 0.6 * semantic_similarity) * 100, 2)

    # Keyword extraction
    feature_names = vectorizer.get_feature_names_out()
    resume_tfidf = tfidf_matrix[0].toarray()[0]
    job_tfidf = tfidf_matrix[1].toarray()[0]

    importance_scores = {
        word: resume_tfidf[i] * job_tfidf[i]
        for i, word in enumerate(feature_names)
        if resume_tfidf[i] > 0 and job_tfidf[i] > 0
    }

    top_keywords = sorted(importance_scores, key=importance_scores.get, reverse=True)[:5]

    return combined_score, top_keywords
