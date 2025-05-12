from typing import Protocol
from fastapi import Request
from pydantic import UUID4

from app.core.models.pydantic_models import GetBill


class CreateBillServiceProtocol(Protocol):
    async def __call__(
        self,
        request: Request,
    ) -> UUID4:
        """Create bill service"""
        pass


class GetBillsServiceProtocol(Protocol):
    async def __call__(
        self,
        request: Request,
    ) -> list[GetBill]:
        """Get bills service"""
        pass


class GetBillServiceProtocol(Protocol):
    async def __call__(
        self,
        bill_id: UUID4,
    ) -> GetBill:
        """Get bill service"""
        pass


class PaymentServiceProtocol(Protocol):
    async def __call__(
        self,
        bill_id: UUID4,
        amount: float,
    ) -> GetBill:
        """Payment Service"""
        pass
