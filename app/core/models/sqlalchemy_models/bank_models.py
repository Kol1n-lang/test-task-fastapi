import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from .base_model import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.core.models.sqlalchemy_models import User


class Bill(Base):
    balance: Mapped[float] = mapped_column(default=0)
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="bills")
    bill_transactions: Mapped[list["BillTransaction"]] = relationship(
        back_populates="bill"
    )


class BillTransaction(Base):
    amount: Mapped[float] = mapped_column(default=0)
    bill_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("bill.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )

    bill: Mapped["Bill"] = relationship(back_populates="bill_transactions")
