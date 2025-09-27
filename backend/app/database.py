from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")
client = AsyncIOMotorClient(os.getenv("MONGO_URL"))


db = client.resume
users_collection = db.get_collection("users")
resumes_collection = db.get_collection("resumes")
