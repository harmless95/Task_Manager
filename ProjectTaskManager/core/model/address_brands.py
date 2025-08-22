from uuid import UUID
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUID_PG

from .base import Base
from .mixins.uuid_pr_key import KeyUUID

if TYPE_CHECKING:
    from .address import Address
    from .brand_car import Brand


class AddressBrands(Base, KeyUUID):
    __tablename__ = "address_brands"
    __table_args__ = (
        UniqueConstraint(
            "address_id",
            "brands_id",
            name="idx_unique_address_brands",
        ),
    )

    address_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("addresss.id")
    )
    brands_id: Mapped[UUID] = mapped_column(
        UUID_PG(as_uuid=True), ForeignKey("brands.id")
    )

    address: Mapped["Address"] = relationship(" Address", back_populates="brands")
    brand: Mapped["Brand"] = relationship("Brand", back_populates="addresses")
