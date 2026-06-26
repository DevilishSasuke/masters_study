from datetime import datetime

from warehouse.db import Base, int_pk, str_uniq
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, CheckConstraint

class Item(Base):
    __tablename__ = "items"

    id: Mapped[int_pk]
    name: Mapped[str_uniq]
    amount: Mapped[int] = mapped_column(default=1)

    __table_args__ = (
        CheckConstraint('amount >= 0', name = 'check_amount'),
    )

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int_pk]
    item_name: Mapped[str] = mapped_column(nullable=False)
    amount: Mapped[int] = mapped_column(default=1)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    __table_args__ = (
        CheckConstraint('amount >= 0', name = 'check_amount_order'),
    )
