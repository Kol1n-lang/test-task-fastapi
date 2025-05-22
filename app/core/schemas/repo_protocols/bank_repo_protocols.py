from typing import Protocol
from pydantic import UUID4

from app.core.models.sqlalchemy_models import Bill


class BankRepoProtocol(Protocol):

    async def create_bill(self, user_id: UUID4) -> UUID4:
        """Create bill in database"""
        pass

    async def get_user_id(self, email: str, username: str) -> UUID4:
        """Find uuid for creating bill"""
        pass

    async def get_user_bills(self, bill_id: UUID4) -> list[Bill]:
        """Find all users bills in database"""
        pass

    async def get_user_bill(self, bill_id: UUID4) -> Bill:
        """Find bill in database"""
        pass

    async def payment(self, bill_id: UUID4, amount: float) -> Bill:
        """Del money in bill"""
        pass

    async def create_transaction(self, bill_id: UUID4, amount: float) -> None:
        """Create transaction in database"""
        pass
