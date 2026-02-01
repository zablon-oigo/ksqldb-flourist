from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
import uuid


class UserCreateModel(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str
    role: Optional[str] = "user"

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "email": "johndoe123@co.com",
                "password": "testpass123",
                "role": "user"
            }
        }
    }


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
