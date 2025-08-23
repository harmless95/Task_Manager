from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

from .base import Base
from .mixins.uuid_pr_key import KeyUUID

if TYPE_CHECKING:
    from .brand_car import Brand


class Car(Base, KeyUUID):
    name: Mapped[str] = mapped_column(String(100), unique=True)
    color: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column()
    brand_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("brands.id")
    )

    brand: Mapped["Brand"] = relationship("Brand", back_populates="cars")
