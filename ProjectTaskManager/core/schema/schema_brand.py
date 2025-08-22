from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from .schema_address import AddressCreate, AddressRead, AddressUpdate


class BrandCreate(BaseModel):
    name: str
    address: Optional["AddressCreate"]

    model_config = ConfigDict(from_attributes=True)


class BrandRead(BaseModel):
    id: UUID
    name: str
    address: Optional["AddressRead"]

    model_config = ConfigDict(from_attributes=True)


class BrandUpdate(BaseModel):
    name: str
    address: Optional["AddressUpdate"]

    model_config = ConfigDict(from_attributes=True)
