from pydantic import UUID4

from app.core.custom_exceptions import (
    UserAlreadyExistsError,
    IncorrectPasswordOrEmailError,
)
from app.core.models.pydantic_models import RegisterUser, LoginUser
from app.core.schemas.repo_protocols import AuthRepoProtocol
from app.core.schemas.service_protocols import JWTServiceProtocol


class RegisterUserService:

    def __init__(self, auth_repo: AuthRepoProtocol):
        self._auth_repo = auth_repo

    async def __call__(self, new_user: RegisterUser) -> UUID4:
        check_user_already_exists = await self._auth_repo.check_user_already_exists(
            new_user.email
        )
        if not check_user_already_exists:
            raise UserAlreadyExistsError
        res = await self._auth_repo.register_user(new_user)
        return res


class LoginService:

    def __init__(
        self,
        auth_repo: AuthRepoProtocol,
        jwt_service: JWTServiceProtocol,
    ):
        self._auth_repo = auth_repo
        self._jwt_service = jwt_service

    async def __call__(self, login_user: LoginUser) -> dict:
        check_user = await self._auth_repo.check_user(
            login_user.email, login_user.password
        )
        if not check_user:
            raise IncorrectPasswordOrEmailError
        jwt_tokens = self._jwt_service.create_access_refresh_tokens(
            {"username": login_user.username, "email": login_user.email}
        )
        return jwt_tokens
