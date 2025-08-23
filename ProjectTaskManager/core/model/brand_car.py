from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


from .mixins.uuid_pr_key import KeyUUID
from .base import Base

if TYPE_CHECKING:
    from .car import Car
    from .address import Address


class Brand(Base, KeyUUID):
    name: Mapped[str] = mapped_column(String(150), unique=True)

    addresses: Mapped[list["Address"]] = relationship(back_populates="brand_a")
    cars: Mapped[list["Car"]] = relationship("Car", back_populates="brand")
