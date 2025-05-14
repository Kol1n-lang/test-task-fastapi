import asyncio
import httpx
import redis.asyncio as redis
from typing import Dict, Any, Optional
from fastapi import HTTPException
from pydantic import UUID4

from app.core.configs import all_settings
from app.core.models.pydantic_models import GetBill


class GetCurrenciesService:
    def __init__(self):
        self.redis = redis.Redis(
            host=all_settings.redis.host,
            port=all_settings.redis.port,
            db=all_settings.redis.db,
            decode_responses=True,
        )
        self.client = httpx.AsyncClient()
        self.api_key = all_settings.external.api_secret_key
        self.base_url = "https://apilayer.net/api/live"

    async def __fetch_rate(self, source_currency: str) -> Dict[str, Any]:
        url = f"{self.base_url}?access_key={self.api_key}&currencies=RUB&source={source_currency}&format=1"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to fetch {source_currency} rate: {str(e)}",
            )

    async def __close(self):
        await self.redis.close()
        await self.client.aclose()

    def __parsing(self, data: dict[str, Any]) -> Optional[str]:
        try:
            if not isinstance(data, dict) or not data.get("success"):
                return None

            quotes = data.get("quotes", {})
            if not isinstance(quotes, dict) or len(quotes) == 0:
                return None

            rate = next(iter(quotes.values()), None)
            return str(rate) if isinstance(rate, (int, float)) else None
        except Exception:
            return None

    async def __caching(self) -> Dict[str, Any]:
        try:
            usd, eur = await asyncio.gather(
                self.redis.get("usd"), self.redis.get("eur")
            )

            if not all([usd, eur]):
                usd_data, eur_data = await asyncio.gather(
                    self.__fetch_rate("USD"), self.__fetch_rate("EUR")
                )

                parsed_usd = self.__parsing(usd_data)
                parsed_eur = self.__parsing(eur_data)

                if parsed_usd is None or parsed_eur is None:
                    return {"usd": parsed_usd, "eur": parsed_eur}
                await asyncio.gather(
                    self.redis.setex("usd", all_settings.redis.cache_time, parsed_usd),
                    self.redis.setex("eur", all_settings.redis.cache_time, parsed_eur),
                )

                return {"usd": parsed_usd, "eur": parsed_eur}

            return {"usd": usd, "eur": eur}
        except redis.RedisError as e:
            raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

    async def __call__(self) -> dict:
        return await self.__caching()


class CachedBillsService:

    def __init__(self):
        self.redis = redis.Redis(
            host=all_settings.redis.host,
            port=all_settings.redis.port,
            db=all_settings.redis.db,
            decode_responses=True,
        )

    async def __call__(self, user_id: UUID4) -> True | False:

        cached_bills = await self.redis.hgetall(str(user_id))
        if not cached_bills:
            return False
        return [
            GetBill.model_validate_json(bill_data)
            for bill_data in cached_bills.values()
        ]

    async def take_cache(self, user_id: UUID4):
        pass

    async def caching(self, user_id: UUID4, user_bills: list[GetBill]) -> None:
        bills_data = {
            str(bill.uuid): bill.model_dump_json()
            for bill in user_bills
        }
        await self.redis.hset(str(user_id), mapping=bills_data)
        await self.redis.expire(str(user_id), 15)