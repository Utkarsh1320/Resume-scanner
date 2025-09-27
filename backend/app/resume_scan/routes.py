from fastapi import APIRouter, Depends, UploadFile
from app.database import resumes_collection
from app.models import Resume
from bson import ObjectId

router = APIRouter()

@router.post("/upload")
async def upload_resume(resume: UploadFile, user_id: str):
    content = await resume.read()
    resume_doc = {
        "filename": resume.filename,
        "text_content": content.decode("utf-8", errors="ignore"),
        "user_id": user_id
    }
    result = await resumes_collection.insert_one(resume_doc)
    return {"message": "Resume uploaded", "resume_id": str(result.inserted_id)}
