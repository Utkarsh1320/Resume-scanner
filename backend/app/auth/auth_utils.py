from http.client import HTTPException

from dotenv import load_dotenv
from fastapi import HTTPException, BackgroundTasks
from fastapi.security import HTTPBearer
from jose import jwt
from passlib.context import CryptContext
import secrets
import os
import sendgrid

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.database import users_collection
from app.models import EmailVerificationRequest, EmailResendRequest

load_dotenv(dotenv_path='app/.env')
ALGORITHM = os.getenv("ALGORITHM")
sender_email = os.getenv("FROM_EMAIL")
sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    return jwt.encode(to_encode, sendgrid_api_key, algorithm=algorithm)


def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)

async def send_verification_email(email: str, token: str):
    if not sendgrid_api_key:
        print(f"Email verification skipped for {email} - SendGrid not configured Problem with API Key")
        return
    
    try:
        verification_url = f"http://127.0.0.1:8000/auth/verify-email?token={token}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 10px; margin-bottom: 30px;">
                <h1 style="color: white; margin: 0; font-size: 28px;">🚀 Utkarsh Resume</h1>
                <p style="color: #e8e8e8; margin: 10px 0 0 0; font-size: 16px;">AI-Powered Resume Optimization</p>
            </div>
            
            <div style="background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                <h2 style="color: #333; margin-bottom: 20px;">Verify Your Email Address</h2>
                <p style="color: #666; line-height: 1.6; margin-bottom: 30px;">
                    Thank you for signing up for ResumeAI! Please click the button below to verify your email address and start optimizing your resume with AI.
                </p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; 
                              padding: 15px 30px; 
                              text-decoration: none; 
                              border-radius: 25px; 
                              font-weight: bold; 
                              display: inline-block;
                              box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">
                        ✅ Verify Email Address
                    </a>
                </div>
                
                <p style="color: #999; font-size: 14px; margin-top: 30px; text-align: center;">
                    If the button doesn't work, copy and paste this link into your browser:<br>
                    <a href="{verification_url}" style="color: #667eea; word-break: break-all;">{verification_url}</a>
                </p>
                
                <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                
                <p style="color: #999; font-size: 12px; text-align: center; margin: 0;">
                    This verification link will expire in 24 hours.<br>
                    If you didn't create an account with ResumeAI, please ignore this email.
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                <p>© 2025 ResumeAI - Empowering careers with AI-powered resume optimization</p>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email=sender_email,
            to_emails=email,
            subject="Verify your email - Resume Scanner",
            html_content=html_content
        )
        
        sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
        response = sg.send(message)
        
        print(f"✅ Email sent successfully to {email} (Status: {response.status_code})")
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        print(f"Error type: {type(e).__name__}")

        # More specific error handling
        if hasattr(e, 'status_code'):
            print(f"Status Code: {e.status_code}")
        if hasattr(e, 'body'):
            print(f"Error Body: {e.body}")
        pass

async def verify_email(request : EmailVerificationRequest):
    user = await users_collection.find_one({"verification_token" : request.token})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    result = await users_collection.update_one(
        {"verification_token" : request.token},
        {"$set" : {"is_verified" : True, "verification_token": ""}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to verify email")

    print(f"✅ Email verified successfully for user: {user.get('email')}")
    return {"message" : "Email verified successfully"}

async def resend_verification_email(background_tasks: BackgroundTasks, request: EmailResendRequest):
    user = await users_collection.find_one({"email": request.email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if user.get("is_verified", False):
        raise HTTPException(status_code=400, detail="Email already verified")
    new_token = generate_verification_token()
    result = await users_collection.update_one(
        {"email" : user["email"]},
        {"$set": {"verification_token": new_token}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update verification token")
    background_tasks.add_task(send_verification_email, request.email, new_token)
    print(f"✅ Resent verification email to {request.email}")
    return {"messages" : "Verification email sent successfully"}

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     try:
#         payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"]):
