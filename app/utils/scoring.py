from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import logging

logger = logging.getLogger(__name__)

def create_tfidf_matrix(corpus):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    return tfidf_matrix

def calculate_scores(job_desc, resumes, resume_data):
    try:
        corpus = [job_desc] + resumes
        tfidf_matrix = create_tfidf_matrix(corpus)
        if tfidf_matrix is None:
            return [0] * len(resumes)
        
        cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        similarity_scores = cos_sim[0]
        normalized_sim = similarity_scores / np.max(similarity_scores) if np.max(similarity_scores) > 0 else similarity_scores

        exp_scores = [min(r['experience'] / 10, 1.0) for r in resume_data]

        skill_match_scores = []
        job_skills = set(job_desc.split())  # Optional: replace with NLP extraction

        for resume in resume_data:
            resume_skills = set(resume['skills'])
            match_count = len(job_skills.intersection(resume_skills))
            skill_match_scores.append(min(match_count / 10, 1.0))

        final_scores = [
            0.7 * normalized_sim[i] +
            0.2 * exp_scores[i] +
            0.1 * skill_match_scores[i]
            for i in range(len(resumes))
        ]

        return [min(score * 100, 100) for score in final_scores]
    
    except Exception as e:
        logger.error(f"Error calculating scores: {str(e)}")
        return [0] * len(resumes)
