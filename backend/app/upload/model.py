from bson import ObjectId

def serialize_resume(resume) -> dict:
    """Convert MongoDB resume doc into JSON serializable dict"""
    return {
        "resume_id": str(resume["_id"]),
        "filename": resume["filename"],
        "text_content": resume["text_content"],
        "user_id": resume["user_id"],
    }
