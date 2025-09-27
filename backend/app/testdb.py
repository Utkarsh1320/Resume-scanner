from fastapi import APIRouter
from app.db import users_collection

router = APIRouter()

@router.get("/ping-db")
async def ping_db():
    user_count = await users_collection.count_documents({})
    return {"connected": True, "user_count": user_count}
