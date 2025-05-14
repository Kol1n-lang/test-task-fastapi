from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from fastapi import Request
from jose import jwt

from app.core.configs import all_settings
from app.core.custom_exceptions import (
    JWTIsEmptyError,
    InvalidTokenError,
    JWTIsFiredError,
)
from app.core.configs.constants import ACCESS_TOKEN

from datetime import datetime, timezone


class JWTAccessMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.excluded_paths = [
            "/docs",
            "/openapi.json",
            "/v1/auth/login",
            "/v1/auth/register",
        ]

    async def dispatch(self, request: Request, call_next):

        for path in self.excluded_paths:
            if path in request.url.path:
                return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise JWTIsEmptyError

        if not auth_header or not auth_header.startswith("Bearer "):
            raise InvalidTokenError
        token = auth_header.split(" ", 1)[1]
        try:
            token_payload: dict = jwt.decode(
                token,
                all_settings.jwt.secret_key,
                algorithms=all_settings.jwt.algorithm,
            )
        except Exception:
            raise InvalidTokenError

        token_type = token_payload.get("type")
        if token_type != ACCESS_TOKEN:
            raise InvalidTokenError

        current_time = datetime.now(timezone.utc).timestamp()
        token_life = token_payload.get("exp")
        if token_life is None:
            raise InvalidTokenError

        if current_time > token_life:
            raise JWTIsFiredError

        return await call_next(request)
