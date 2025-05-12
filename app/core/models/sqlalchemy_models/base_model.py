import uuid
from datetime import datetime
from sqlalchemy import func, UUID, text

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        onupdate=func.now(), default=func.now()
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()
