from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    email: EmailStr
    password: str
    name: str
    is_verified: bool = False
    verification_token: Optional[str] = None
    created_at: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    name: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: Optional[str] = None

class Resume(BaseModel):
    filename: str
    text_content: Optional[str] = None
    user_id: str
    resume_id:str

class EmailVerificationRequest(BaseModel):
    token: str
    
class EmailResendRequest(BaseModel):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str