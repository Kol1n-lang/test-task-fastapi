from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base_model import Base

if TYPE_CHECKING:
    from app.core.models.sqlalchemy_models import Bill


class User(Base):
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)

    bills: Mapped[list["Bill"]] = relationship(back_populates="user")
