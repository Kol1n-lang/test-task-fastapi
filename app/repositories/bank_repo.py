from pydantic import UUID4
from sqlalchemy import select, insert, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.models.sqlalchemy_models import Bill, User, BillTransaction


class BankRepo:

    def __init__(self, con: AsyncSession):
        self._con = con

    async def get_user_id(self, email: str, username: str) -> UUID4:
        query = select(User).where(and_(User.username == username, User.email == email))
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res.id

    async def create_bill(self, user_id: UUID4) -> UUID4:
        query = (
            insert(Bill)
            .values(
                balance=0,
                user_id=user_id,
            )
            .returning(Bill.id)
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def get_user_bills(self, user_id: UUID4) -> list[Bill]:
        query = (
            select(Bill)
            .where(Bill.user_id == user_id)
            .options(selectinload(Bill.user), selectinload(Bill.bill_transactions))
        )
        res = (await self._con.execute(query)).scalars().all()
        return list(res)

    async def get_user_bill(self, bill_id: UUID4) -> Bill:
        query = (
            select(Bill)
            .where(Bill.id == bill_id)
            .options(selectinload(Bill.user), selectinload(Bill.bill_transactions))
        )
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def payment(self, bill_id: UUID4, amount: float) -> Bill:
        if amount > 0:
            query = (
                update(Bill)
                .where(Bill.id == bill_id)
                .values(balance=Bill.balance + amount)
                .options(selectinload(Bill.user), selectinload(Bill.bill_transactions))
            ).returning(Bill)
            query_res = (await self._con.execute(query)).scalar_one()
            return query_res
        query = (
            update(Bill)
            .where(Bill.id == bill_id)
            .where(Bill.balance >= (-1) * amount)
            .values(balance=Bill.balance + amount)
            .options(selectinload(Bill.user), selectinload(Bill.bill_transactions))
        ).returning(Bill)
        query_res = (await self._con.execute(query)).scalar_one()
        return query_res

    async def create_transaction(self, bill_id: UUID4, amount: float) -> None:
        query = insert(BillTransaction).values(
            bill_id=bill_id,
            amount=amount,
        )
        await self._con.execute(query)
