from pydantic import BaseModel
from typing import Optional

class ResumeUploadResponse(BaseModel):
    message: str
    resume_id: str

class ResumeInDB(BaseModel):
    filename: str
    text_content: str
    user_id: Optional[str] = None
    resume_id: Optional[str] = None
