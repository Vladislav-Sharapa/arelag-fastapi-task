from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.core.models import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    status: Mapped[str] = mapped_column(nullable=True)

    user_balance: Mapped[List["UserBalance"]] = relationship("UserBalance", back_populates="owner")


class UserBalance(BaseModel):
    __tablename__ = "user_balance"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    currency: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[Decimal] = mapped_column(default=0, nullable=True)

    __table_args__ = (UniqueConstraint("user_id", "currency", name="user_balance_user_currency_unique"),)
    owner: Mapped["User"] = relationship("User", back_populates="user_balance")
