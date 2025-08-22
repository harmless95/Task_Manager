from uuid import UUID
from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    country: str
    city: str
    street: str
    house: str

    model_config = ConfigDict(from_attributes=True)


class AddressRead(BaseModel):
    id: UUID
    country: str
    city: str
    street: str
    house: str

    model_config = ConfigDict(from_attributes=True)


class AddressUpdate(BaseModel):
    country: str | None = None
    city: str | None = None
    street: str | None = None
    house: str | None = None

    model_config = ConfigDict(from_attributes=True)
