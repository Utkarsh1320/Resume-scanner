from fastapi import HTTPException, BackgroundTasks
from app.models import User, UserCreate, UserLogin, UserResponse, TokenResponse, EmailVerificationRequest, \
    EmailResendRequest
from app.database import users_collection
from app.auth.auth_utils import hash_password, verify_password, create_access_token, send_verification_email, \
    verify_email as verify_email_util, resend_verification_email as resend_verification_email_util
from datetime import datetime, timezone
import secrets


def generate_verification_token():
    return secrets.token_urlsafe(32)


class UserService:

    @staticmethod
    async def register_user(background_tasks: BackgroundTasks, user: UserCreate) -> dict[str, str]:
        existing_user = await users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        verification_token = generate_verification_token()

        hashed_password = hash_password(user.password)

        user_dict = {
            "email": user.email,
            "password": hashed_password,
            "name": user.name,
            "is_verified": False,
            "verification_token": verification_token,
            "created_at": datetime.now(timezone.utc),
        }

        result = await users_collection.insert_one(user_dict)
        background_tasks.add_task(send_verification_email, user.email, verification_token)

        return {"message": "User registered successfully. Please check your email to verify your account."}

    @staticmethod
    async def login_user(user: UserLogin) -> TokenResponse:
        db_user = await users_collection.find_one({"email": user.email})
        if not db_user or not verify_password(user.password, db_user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check if user is verified
        if not db_user.get("is_verified", False):
            raise HTTPException(status_code=401, detail="Please verify your email first")

        access_token = create_access_token(data={"sub": str(db_user["_id"])})
        return TokenResponse(
            access_token=access_token,
            user_id=str(db_user["_id"])
        )

    @staticmethod
    async def verify_email(request : EmailVerificationRequest) -> dict[str, str]:
        return await verify_email_util(request)

    @staticmethod
    async def resend_verification_email(background_tasks: BackgroundTasks,  request: EmailResendRequest) -> dict[str, str]:
        return await resend_verification_email_util(background_tasks,request)

