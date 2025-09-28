from .utils import extract_keywords, calculate_similarity, keyword_occurrences

async def scan_resume_service(resume_text: str, job_description: str) -> dict:
    """Scan resume against job description and return ATS score and keyword counts."""
    job_keywords = extract_keywords(job_description)
    resume_keywords = keyword_occurrences(resume_text, job_keywords)
    ats_score = calculate_similarity(resume_text, job_description)

    return {
        "ats_score": round(ats_score, 2),
        "resume_keywords": resume_keywords,
        "job_keywords": job_keywords
    }
