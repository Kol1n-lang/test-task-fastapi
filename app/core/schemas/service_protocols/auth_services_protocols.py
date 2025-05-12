from typing import Protocol

from pydantic import UUID4

from app.core.models.pydantic_models import RegisterUser, LoginUser


class RegisterUserServiceProtocol(Protocol):
    async def __call__(self, new_user: RegisterUser) -> UUID4:
        """Register a new user"""
        pass


class LoginServiceProtocol(Protocol):
    async def __call__(self, login_user: LoginUser) -> dict:
        """Create jwt token if user is correct"""
        pass
