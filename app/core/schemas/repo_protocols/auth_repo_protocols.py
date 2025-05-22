from typing import Protocol

from pydantic import UUID4, EmailStr

from app.core.models.pydantic_models import RegisterUser


class AuthRepoProtocol(Protocol):
    async def register_user(self, new_user: RegisterUser) -> UUID4:
        """Create new user in Database"""
        pass

    async def check_user_already_exists(self, user_email: EmailStr) -> bool:
        """Check user already exists in Database"""
        pass

    async def _hash_password(self, password: str) -> bytes:
        """Hash password"""
        pass

    async def _check_password(self, password: str, hashed_password: bytes) -> bool:
        """Check password against hashed password"""
        pass

    async def check_user(self, email: EmailStr, password: str) -> bool:
        """Check user exists in Database"""
        pass
