from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.resume_scan.routes import router as resume_router

app = FastAPI(title="Resume Scanner MongoDB")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(resume_router, prefix="/resume", tags=["resume"])
