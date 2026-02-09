from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta, timezone

from src.db.main import get_session
from src.db.redis import add_jti_to_blocklist
from .schemas import PasswordResetConfirmModel, PasswordResetRequestModel, UserCreateModel, UserLoginModel, UserModel, UserBooksModel
from .services import UserService
from .utils import verify_password, create_access_token, generate_password_hash
from src.celery import send_email  
from src.auth.schemas import SignupResponseModel
from src.errors import UserNotFound, UserAlreadyExists
from src.config import Config


from src.auth.utils import (
    create_url_safe_token,
    decode_url_safe_token,
)

from .dependencies import (
    AccessTokenBearer,
    RefreshTokenBearer,
    RoleChecker,
    get_current_user,
)

role_checker = RoleChecker(["admin","user"])
admin_checker = RoleChecker(["admin"])
auth_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY_DAYS = 7  

refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()



@auth_router.post("/signup", response_model=SignupResponseModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session),
):
    email = user_data.email.lower()

    if await user_service.user_exists(email, session):
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}"
    html = f"""
    <h1>Welcome to {Config.APP_NAME}</h1>
    <p>Hi {new_user.username},</p>
    <p>Thank you for registering at {Config.APP_NAME}.</p>
    <p>Click the link below to verify your email:</p>
    <p>Please click this <a href="{link}">link</a> to verify your email</p>
    <p>If you did not sign up, you can safely ignore this email.</p>
    """
    send_email.delay([email], "Verify Your Email", html)

    return {
        "message": "Account created.Check your email to verify your account.",
        "user": new_user,
    }


