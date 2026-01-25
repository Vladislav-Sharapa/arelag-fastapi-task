from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.src.core.models import BaseModel
from app.src.models.user import User


class Transaction(BaseModel):
    __tablename__ = "transaction"

    user_id: Mapped[int] = mapped_column(nullable=False)
    currency: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[Decimal] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=True)

    owner: Mapped["User"] = relationship("User", back_populates="user_balance")
