import uuid
import logging
from datetime import datetime, timedelta, timezone
from itsdangerous import URLSafeTimedSerializer
from itsdangerous import BadSignature, SignatureExpired
from fastapi import HTTPException

import jwt
from passlib.context import CryptContext
from src.config import Config

serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET, 
    salt="email-configuration"
)

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_password_hash(password: str) -> str:
    return passwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)


def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False) -> str:
    payload = {
        "user": user_data,
        "exp": datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(minutes=60)),
        "jti": str(uuid.uuid4()),
        "refresh": refresh
    }
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )
    return token

def decode_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as jwte:
        logging.exception("JWT decode error", exc_info=jwte)
        return None
    except Exception as e:
        logging.exception("Unknown error decoding JWT", exc_info=e)
        return None



def create_url_safe_token(data: dict) -> str:

    try:
        token = serializer.dumps(data)
        return token
    except Exception as e:
        logging.error(f"Error creating token: {str(e)}")
        raise HTTPException(status_code=500, detail="Could not create token")

def decode_url_safe_token(token: str, max_age: int = 3600) -> dict:

    try:
        data = serializer.loads(token, max_age=max_age)
        return data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")
    except Exception as e:
        logging.exception("Unknown error decoding token", exc_info=e)
        raise HTTPException(status_code=500, detail="Could not decode token")
    