from decimal import Decimal

from sqlalchemy import Column, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.model import Base


class Transaction(Base):
    __tablename__ = "transaction"

    user_id: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[Decimal] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)
