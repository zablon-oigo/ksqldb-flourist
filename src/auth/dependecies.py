from typing import List
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.db.main import get_session
from src.db.models import User
from src.db.redis import token_in_blocklist
from src.auth.services import UserService
from src.auth.utils import decode_token
from src.errors import (
    InvalidToken,
    RefreshTokenRequired,
    AccessTokenRequired,
    InsufficientPermission,
    UserNotFound,
    AccountNotVerified
)

user_service = UserService()


class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds: HTTPAuthorizationCredentials = await super().__call__(request)

        if not creds or not creds.credentials:
            raise InvalidToken("Authorization token missing")

        token = creds.credentials
        token_data = decode_token(token)

        if not token_data:
            raise InvalidToken("Could not decode token or token is malformed")

        if await token_in_blocklist(token_data.get("jti")):
            raise InvalidToken("Token has been revoked or is invalid")

        self.verify_token_data(token_data)
        return token_data

    def verify_token_data(self, token_data: dict) -> None:
        raise NotImplementedError("Override this method in child classes")


class AccessTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if token_data.get("refresh", False):
            raise AccessTokenRequired("Expected an access token, not a refresh token")


class RefreshTokenBearer(TokenBearer):

    def verify_token_data(self, token_data: dict) -> None:
        if not token_data.get("refresh", False):
            raise RefreshTokenRequired("Expected a refresh token, not an access token")


