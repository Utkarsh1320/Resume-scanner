from typing import Any, Coroutine

from bson import ObjectId

from app.database import resumes_collection
from app.upload.utlis import extract_text_from_file

from app.database import users_collection
from fastapi import HTTPException


async def save_resume(file, user_id: str) -> str:
    # Validate user_id
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status_code=400, detail="Invalid user ID")

    # Fetch the user
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Read file content
    file_content = await file.read()
    text_content = await extract_text_from_file(file_content, file.filename)

    # Prepare resume document
    resume_doc = {
        "filename": file.filename,
        "text_content": text_content,
        "user_id": user_id,  # store as string for simplicity
    }

    # Insert into MongoDB
    result = await resumes_collection.insert_one(resume_doc)
    return str(result.inserted_id)

async def get_resume(resume_id:str) -> Any | None:
    from app.upload.model import serialize_resume

    resume = await resumes_collection.find_one({"_id": ObjectId(resume_id)})
    if resume:
        return serialize_resume(resume)
    return None

