from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as UUID_PG
from sqlalchemy import String, ForeignKey


from .mixins.uuid_pr_key import KeyUUID
from .base import Base

if TYPE_CHECKING:
    from .car import Car
    from .address_brands import AddressBrands


class Brand(Base, KeyUUID):
    name: Mapped[str] = mapped_column(String(150), unique=True)
    address_brand: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("addresss.id")
    )
    addresses: Mapped[list["AddressBrands"]] = relationship(back_populates="brand")
    cars: Mapped[list["Car"]] = relationship("Car", back_populates="brand")
