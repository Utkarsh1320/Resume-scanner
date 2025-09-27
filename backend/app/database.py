from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb+srv://umore9939:Utkarsh1320@cluster1.t0mp1ka.mongodb.net/"

client = AsyncIOMotorClient(MONGO_DETAILS)

db = client.resume
users_collection = db.get_collection("users")
resumes_collection = db.get_collection("resumes")
