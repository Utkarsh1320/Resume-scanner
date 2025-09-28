from pydantic import BaseModel
from typing import Dict, List

class ScanRequest(BaseModel):
    resume_content: str
    job_description: str

class ScanResponse(BaseModel):
    ats_score: float
    resume_keywords: Dict[str, int]
    job_keywords: List[str]
