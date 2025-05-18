from fastapi import APIRouter, Request
from dishka.integrations.fastapi import inject, FromDishka
from pydantic import UUID4

from app.core.models.pydantic_models import GetBill, GetTransaction
from app.core.schemas.service_protocols import (
    CreateBillServiceProtocol,
    GetBillsServiceProtocol,
    GetBillServiceProtocol,
    GetCurrenciesServiceProtocol,
    PaymentServiceProtocol,
)

bank_router = APIRouter(
    prefix="/bank",
    tags=["bank"],
)


@bank_router.post(
    path="/create-bill",
    response_model=UUID4,
    description="Create a new bank bill",
)
@inject
async def create_bank_bill(
    request: Request, create_bill_service: FromDishka[CreateBillServiceProtocol]
) -> UUID4:
    return await create_bill_service(request)


@bank_router.get(
    path="/get-bills",
    response_model=list[GetBill],
)
@inject
async def get_user_bills(
    request: Request,
    get_user_bills_service: FromDishka[GetBillsServiceProtocol],
) -> list[GetBill]:
    return await get_user_bills_service(request)


@bank_router.get(
    path="/get-bills/{bill_id}",
    response_model=GetBill,
)
@inject
async def get_user_bill(
    bill_id: UUID4,
    get_bill_service: FromDishka[GetBillServiceProtocol],
) -> GetBill:
    return await get_bill_service(bill_id)


@bank_router.get(
    path="/get-currencies",
    response_model=dict,
    description="Get currencies",
)
@inject
async def get_currencies(
    get_currencies_service: FromDishka[GetCurrenciesServiceProtocol],
) -> dict:
    return await get_currencies_service()


@bank_router.post(
    path="/payment",
    response_model=GetBill,
)
@inject
async def payment(
    transaction: GetTransaction,
    payment_service: FromDishka[PaymentServiceProtocol],
) -> GetBill:
    return await payment_service(transaction.bill_id, transaction.amount)
