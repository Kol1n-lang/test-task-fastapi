from typing import Protocol, Any, Optional


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
