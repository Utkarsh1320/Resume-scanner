from fastapi import APIRouter, BackgroundTasks
from pyexpat.errors import messages

from app.auth.service import UserService
from app.models import UserCreate, UserLogin, UserResponse, TokenResponse, EmailVerificationRequest, EmailResendRequest

router = APIRouter()

@router.post("/register")
async def register_user(background_tasks: BackgroundTasks, user: UserCreate):
    return await UserService.register_user(background_tasks, user)

@router.post("/login", response_model=TokenResponse)
async def login_user(user: UserLogin):
    return await UserService.login_user(user)

@router.post("/verify-email")
async def verify_email(request: EmailVerificationRequest):
    return await UserService.verify_email(request)

@router.get("/verify-email")
async def verify_email_get(token: str):
    request = EmailVerificationRequest(token=token)
    return await UserService.verify_email(request)

@router.post("/resend-verification")
async def resend_verification_email(background_tasks: BackgroundTasks, request: EmailResendRequest ):
    return await UserService.resend_verification_email(background_tasks, request )
@router.get("/test")
async def test():
    return {"messages" : "test"}