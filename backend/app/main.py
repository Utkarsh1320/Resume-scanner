from fastapi import FastAPI
from app.auth.routes import router as auth_router
from app.upload.routes import router as upload_router
from app.scan.routes import router as scan_router

app = FastAPI(title="Resume Scanner MongoDB")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(upload_router, prefix="/upload", tags=["upload"])
app.include_router(scan_router, prefix="/scan", tags=["scan"])