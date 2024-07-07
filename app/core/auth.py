"""Adapted from quivr_api/middlewares/auth/auth.py

Used under the terms of the Apache 2.0 License
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid6 import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import JWTError
from pydantic import ValidationError

from app.core.config import settings

from app.modules.base.schema import UserIdentity, ApiKeyIdentity, SupabaseAccessToken
from app.core.log import make_logger

ALGORITHM = "HS256"
TEST_API_KEY = ApiKeyIdentity(api_key="fake-test-api-key")

logger = make_logger(__name__)

"""this is by no means a complete auth implementation.
among other things, it only verifies that provided tokens were signed
by the given JWT secret for authentication. integrate this with 
an actual auth provider like supabase to provide full auth
"""


class AuthBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(
        self,
        request: Request,
    ) -> ApiKeyIdentity:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        self.check_scheme(credentials)
        token = credentials.credentials  # pyright: ignore reportPrivateUsage=none
        return await self.authenticate(token)

    def check_scheme(self, credentials):
        if credentials and credentials.scheme != "Bearer":
            raise HTTPException(status_code=401, detail="Token must be Bearer")
        elif not credentials:
            raise HTTPException(
                status_code=403, detail="Authentication credentials missing"
            )

    async def authenticate(
        self,
        token: str,
    ) -> ApiKeyIdentity:
        if not settings.AUTHENTICATION_ENABLED:
            return TEST_API_KEY
        elif identity := (is_api_token(token)): #or is_supabase_token(token))
            return identity
        else:
            raise HTTPException(status_code=401, detail="Invalid token or API key.")


def get_current_user(user: ApiKeyIdentity = Depends(AuthBearer())) -> ApiKeyIdentity:
    return user


def _encode_jwt(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.AUTH_JWT_SECRET, algorithm=ALGORITHM
    )
    return encoded_jwt


def create_access_token(user: dict[str, str]) -> str:
    return _encode_jwt(data=user, expires_delta=timedelta(minutes=30))


def _decode_jwt(token: str) -> UserIdentity | None:
    try:
        payload = jwt.decode(
            token,
            settings.AUTH_JWT_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},
        )
        return payload
    except JWTError as e:
        logger.error("Failed to decode access token: %s", e, exc_info=e)
        return None


# def is_supabase_token(token: str) -> UserIdentity | None:
#     payload = _decode_jwt(token)
#     if not payload:
#         return None

#     try:
#         user = SupabaseAccessToken.model_validate(payload)
#         return UserIdentity(email=user.email, id=UUID(user.sub))
#     except ValidationError:
#         return None


def is_api_token(token: str) -> ApiKeyIdentity | None:
    payload = _decode_jwt(token)
    if not payload:
        return None

    if api_key := payload.get("api_key", None):
        return ApiKeyIdentity(
            api_key=api_key,
        )
    else:
        app_metadata = payload.get("app_metadata", None)
        if api_key := app_metadata.get("api_key", None):
            return ApiKeyIdentity(api_key=api_key)

    return None


# def is_supabase_anon_token(token: str) -> UserIdentity | None:
#     payload = _decode_jwt(token)
#     conditions = (
#         payload.get("iss") == "supabase",
#         # check the supabase project id from the url
#         payload.get("ref") == settings.SUPABASE_URL.split(1)[0],
#         payload.get("role") == "anon",
#     )
#     if all(conditions):
#         return TEST_USER

#     return None


# def is_supabase_service_token(token: str) -> UserIdentity | None:
#     payload = _decode_jwt(token)
#     conditions = (
#         payload.get("iss") == "supabase",
#         payload.get("ref") == settings.SUPABASE_URL.split(1)[0],
#         payload.get("role") == "service_role",
#     )

#     if all(conditions):
#         # not yet sure how to represent service user correctly
#         return "SERVICE_USER"

#     return None
