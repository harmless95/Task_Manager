from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

from .mixins.uuid_pr_key import KeyUUID
from .base import Base

if TYPE_CHECKING:
    from .address_brands import AddressBrands


class Address(Base, KeyUUID):
    country: Mapped[str] = mapped_column(String(150), unique=True)
    city: Mapped[str] = mapped_column(String(150))
    street: Mapped[str] = mapped_column(String(200))
    house: Mapped[str] = mapped_column()
    brand_name: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("brands.id")
    )

    brands: Mapped[list["AddressBrands"]] = relationship(back_populates="address")
