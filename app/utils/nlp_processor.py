# nlp_processor.py

import spacy
import en_core_web_lg
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from dateutil import parser
from datetime import datetime
import logging
from fuzzywuzzy import fuzz
from .known_skills import known_skills

# Load spaCy model
try:
    nlp = en_core_web_lg.load()
except:
    nlp = spacy.load("en_core_web_lg")

logger = logging.getLogger(__name__)

# Normalize known skills once
normalized_skills = [skill.lower() for skill in known_skills]

def preprocess_text(text):
    try:
        doc = nlp(text)
        tokens = [token.lemma_.lower() for token in doc
                  if not token.is_stop and not token.is_punct and token.is_alpha]
        return " ".join(tokens)
    except Exception as e:
        logger.error(f"Error preprocessing text: {str(e)}")
        return ""


def extract_skills(text):
    try:
        doc = nlp(text)
        found_skills = set()

        phrases = set(chunk.text.lower() for chunk in doc.noun_chunks)
        entities = set(ent.text.lower() for ent in doc.ents if ent.label_ in ["SKILL", "ORG", "PRODUCT"])

        all_candidates = phrases.union(entities)

        for phrase in all_candidates:
            for known in normalized_skills:
                if fuzz.token_set_ratio(phrase, known) >= 85:
                    found_skills.add(known)

        return found_skills
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        return set()


def extract_experience(text):
    experience = 0
    pattern = r'(\d+)\s?\+?\s?(years?|yrs?)\s+experience'
    matches = re.findall(pattern, text, re.IGNORECASE)

    for match in matches:
        try:
            years = int(match[0])
            if years > experience:
                experience = years
        except:
            continue

    if experience == 0:
        date_pattern = r'(\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b|\b\d{4}\b)'
        dates = re.findall(date_pattern, text)
        parsed_dates = []

        for date_str in dates:
            try:
                parsed_date = parser.parse(date_str, fuzzy=True)
                parsed_dates.append(parsed_date)
            except:
                continue

        if len(parsed_dates) >= 2:
            sorted_dates = sorted(parsed_dates)
            total_experience = (sorted_dates[-1] - sorted_dates[0]).days / 365.25
            experience = max(experience, total_experience)

    return min(experience, 20)


def create_tfidf_matrix(corpus):
    vectorizer = TfidfVectorizer()
    try:
        return vectorizer.fit_transform(corpus)
    except Exception as e:
        logger.error(f"Error creating TF-IDF matrix: {str(e)}")
        return None
