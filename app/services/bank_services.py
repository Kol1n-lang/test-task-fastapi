from faststream.rabbit import RabbitBroker
from pydantic import UUID4
from fastapi import Request

from app.core.models.pydantic_models import GetBill
from app.core.schemas.repo_protocols import BankRepoProtocol
from app.core.schemas.service_protocols import CachedBillsServiceProtocol
from app.core.schemas.service_protocols.jwt_service_repo_protocols import (
    JWTServiceProtocol,
)
from app.core.configs import all_settings


class CreateBillService:

    def __init__(
        self, bill_repo: BankRepoProtocol, jwt_service: JWTServiceProtocol
    ) -> None:
        self._bill_repo = bill_repo
        self._jwt_service = jwt_service

    async def __call__(self, request: Request) -> UUID4:
        token = request.headers.get("Authorization")
        user_data = self._jwt_service.get_info_from_token(token)
        username = user_data["username"]
        email = user_data["email"]
        user_id = await self._bill_repo.get_user_id(email, username)
        res = await self._bill_repo.create_bill(user_id)
        return res


class GetBillsService:

    def __init__(
        self,
        bill_repo: BankRepoProtocol,
        jwt_service: JWTServiceProtocol,
        cached_service: CachedBillsServiceProtocol,
    ) -> None:
        self._bill_repo = bill_repo
        self._jwt_service = jwt_service
        self._cached_service = cached_service

    async def __call__(self, request: Request) -> list[GetBill]:
        token = request.headers.get("Authorization")
        user_data = self._jwt_service.get_info_from_token(token)
        username = user_data["username"]
        email = user_data["email"]
        user_id = await self._bill_repo.get_user_id(email, username)
        cached_bills = await self._cached_service(user_id)
        if cached_bills:
            return cached_bills
        res = [
            GetBill.model_validate(bill)
            for bill in await self._bill_repo.get_user_bills(user_id)
        ]
        await self._cached_service.caching(user_id, res)
        return res


class GetBillService:
    def __init__(
        self,
        bill_repo: BankRepoProtocol,
    ) -> None:
        self._bill_repo = bill_repo

    async def __call__(self, bill_id: UUID4) -> GetBill:
        res = await self._bill_repo.get_user_bill(bill_id)
        return GetBill.model_validate(res)


class PaymentService:

    def __init__(
        self,
        bill_repo: BankRepoProtocol,
    ) -> None:
        self._bill_repo = bill_repo

    async def __call__(self, bill_id: UUID4, amount: float) -> GetBill:
        res = await self._bill_repo.payment(bill_id, amount)
        await self._bill_repo.create_transaction(bill_id, amount)
        await self.__publish_message_transaction(str(res.user.email), amount)
        print(str(res.user.email))
        return GetBill.model_validate(res)

    async def __publish_message_transaction(
        self, user_email: str, amount: float
    ) -> None:
        async with RabbitBroker(all_settings.rabbit.rabbit_url) as broker:
            data = {
                "user_email": user_email,
                "amount": amount,
            }
            await broker.publish(data, queue="bank-transactions")  # type: ignore
