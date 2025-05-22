from typing import Protocol, Any, Optional

from pydantic.v1 import UUID4

from app.core.models.pydantic_models import GetBill


class GetCurrenciesServiceProtocol(Protocol):

    async def __call__(self) -> dict:
        """Get cached currencies"""
        pass

    async def __close(self) -> None:
        """Close redis connection, AsyncHttpxClient"""
        pass

    async def __fetch_rate(self, source_currency: str) -> dict[str, Any]:
        """Get cached currency"""
        pass

    async def __caching(self) -> dict[str, Any]:
        """Get cached currencies"""
        pass

    def __parsing(self, data: dict[str, Any]) -> Optional[str]:
        """Parse data"""
        pass


class CachedBillsServiceProtocol(Protocol):

    async def __call__(self, user_id: UUID4) -> list[GetBill] | None:
        """Check cached bills"""
        pass

    async def caching(self, user_id: UUID4, user_bills: list[GetBill]) -> None:
        """Caching bills"""
        pass
