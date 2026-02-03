from decimal import Decimal
from typing import List

from sqlalchemy import ForeignKey, Transaction, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from app.src.core.models import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=True)

    roles: Mapped[List["Role"]] = relationship("Role", back_populates="owner")
    user_balance: Mapped[List["UserBalance"]] = relationship(
        "UserBalance", back_populates="owner"
    )
    transaction: Mapped[List["Transaction"]] = relationship(
        "Transaction", back_populates="owner"
    )

    @hybrid_property
    def fullname(self):
        return f"{self.first_name} {self.last_name}"


class Role(BaseModel):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="roles")


class UserBalance(BaseModel):
    __tablename__ = "user_balance"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    currency: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[Decimal] = mapped_column(default=0, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "user_id", "currency", name="user_balance_user_currency_unique"
        ),
    )
    owner: Mapped["User"] = relationship("User", back_populates="user_balance")
