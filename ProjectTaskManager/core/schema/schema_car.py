from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from .schema_brand import BrandCreate, BrandRead, BrandUpdate


class CarCreate(BaseModel):
    name: str
    color: str
    price: int
    brand_name: Optional["BrandCreate"]

    model_config = ConfigDict(from_attributes=True)


class CarRead(BaseModel):
    id: UUID
    name: str
    color: str
    price: int
    brand_name: Optional["BrandRead"]

    model_config = ConfigDict(from_attributes=True)


class CarUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    price: int | None = None
    brand_name: Optional["BrandUpdate"] | None = None

    model_config = ConfigDict(from_attributes=True)
