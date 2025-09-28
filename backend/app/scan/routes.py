from fastapi import APIRouter, Form, HTTPException
from app.scan.schema import ScanResponse

from app.scan.service import scan_resume_service

router = APIRouter()


@router.post("/", response_model=ScanResponse)
async def scan_resume(
        resume_content: str = Form(...),
        job_description: str = Form(...)
):
    """Scan resume against a job description and return ATS score + keyword occurrences."""
    if not resume_content.strip() or not job_description.strip():
        raise HTTPException(status_code=400, detail="Missing resume content or job description.")

    result = await scan_resume_service(resume_content, job_description)
    return result
