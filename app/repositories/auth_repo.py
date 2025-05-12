import bcrypt
from pydantic import EmailStr, UUID4
from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models.pydantic_models import RegisterUser
from app.core.models.sqlalchemy_models import User


class AuthRepo:
    def __init__(self, con: AsyncSession):
        self._con = con

    async def register_user(self, new_user: RegisterUser) -> UUID4:
        query = (
            insert(User).values(
                email=new_user.email,
                password=self._hash_password(new_user.password),
                username=new_user.username,
            )
        ).returning(User.id)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def check_user_already_exists(self, email: EmailStr) -> bool:
        query = select(User).where(User.email == email)
        query_res = (await self._con.execute(query)).scalar_one_or_none()
        return query_res is None

    def _hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        return bcrypt.hashpw(pwd_bytes, salt=salt)

    async def check_user(self, email: EmailStr, password: str) -> bool:
        query = select(User).where(
            and_(
                User.email == email,
                User.password == self._hash_password(password),
            )
        )
        query_res = (await self._con.execute(query)).scalar_one_or_none
        return query_res is None
