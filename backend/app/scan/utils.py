import spacy
from collections import Counter
import re

nlp = spacy.load("en_core_web_md")

def extract_keywords(text: str, top_n: int = 20) -> list[str]:
    doc = nlp(text)
    keywords = []

    for chunk in doc.noun_chunks:
        # split multi-word chunks into smaller phrases
        for token in chunk:
            if not token.is_stop and token.is_alpha:
                keywords.append(token.text.lower())

    for ent in doc.ents:
        # Include entities as well
        ent_text = re.sub(r"[^\w\s]", "", ent.text.lower())  # remove punctuation
        for token in ent_text.split():
            if token not in nlp.Defaults.stop_words:
                keywords.append(token)

    # count frequency and return top_n unique keywords
    counter = Counter(keywords)
    most_common = [k for k, _ in counter.most_common(top_n)]
    return most_common

def keyword_occurrences(resume_text: str, keywords: list[str]) -> dict[str, int]:
    resume_lower = resume_text.lower()
    occurrences = {}
    for kw in keywords:
        # Count occurrences of whole words only
        occurrences[kw] = len(re.findall(rf"\b{re.escape(kw)}\b", resume_lower))
    return occurrences


def calculate_similarity(resume_text: str, job_description: str) -> float:
    """Return a similarity score between resume and job description."""
    resume_doc = nlp(resume_text)
    job_doc = nlp(job_description)
    return resume_doc.similarity(job_doc)
