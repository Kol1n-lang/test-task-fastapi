from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject
from pydantic import UUID4

from app.core.models.pydantic_models import RegisterUser, LoginUser
from app.core.schemas.service_protocols import (
    RegisterUserServiceProtocol,
)
from app.core.schemas.service_protocols.auth_services_protocols import (
    LoginServiceProtocol,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    path="/register",
    response_model=UUID4,
    description="Register a new user",
)
@inject
async def register(
    register_user: RegisterUser,
    register_service: FromDishka[RegisterUserServiceProtocol],
) -> UUID4:
    return await register_service(register_user)


@auth_router.post(
    path="/login",
    response_model=dict,
    description="Login a user",
)
@inject
async def login(
    login_user: LoginUser,
    login_user_service: FromDishka[LoginServiceProtocol],
) -> dict:
    return await login_user_service(login_user)


@auth_router.get(path="/hello")
async def hello():
    return {"hello": "world"}
