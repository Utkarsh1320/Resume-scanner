from fastapi import APIRouter, UploadFile, HTTPException
from app.upload.service import save_resume, get_resume
from app.upload.schema import ResumeInDB, ResumeUploadResponse

router = APIRouter()
@router.post("/resume", response_model=ResumeInDB, summary="Upload a resume")
async def upload_resume(resume: UploadFile, user_id: str):
    resume_id = await save_resume(resume, user_id)

    resume_data = await get_resume(resume_id)
    if not resume_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve resume")

    # Remove internal ID before returning
    resume_data.pop("user_id", None)
    resume_data.pop("resume_id", None)
    return resume_data

@router.get("/{resume_id}", response_model=ResumeInDB, summary="Fetch a resume by ID")
async def fetch_resume(resume_id: str):
    resume = await get_resume(resume_id)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
