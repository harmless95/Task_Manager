from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import HTTPException, status

from api.CRUD.crud_address import check_address
from core.model import Car, Brand, Address
from core.schema.schema_car import CarUpdate


async def get_cars(
    session: AsyncSession,
) -> list[Car]:
    stmt = select(Car).options(selectinload(Car.brand_name)).order_by(Car.id)
    result = await session.scalars(stmt)
    cars = result.all()
    return list(cars)


async def get_car(session: AsyncSession, car_id: UUID) -> Car:
    stmt = select(Car).options(selectinload(Car.brand_name)).where(Car.id == car_id)
    result = await session.scalars(stmt)
    car = result.first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Invalid id: {car_id!r} not found",
        )
    return car


async def update_car(
    data_update: CarUpdate,
    session: AsyncSession,
    car: Car,
    partial: bool = False,
) -> Car:
    for name, value in data_update.model_dump(exclude_unset=partial).items():
        if isinstance(value, dict) and name == "brand_name":
            brand_n = value.get("name")
            stmt = select(Brand).where(Brand.name == brand_n)
            result = await session.scalars(stmt)
            brand = result.first()
            if not brand:
                address_brand = value.get("address")
                address = await check_address(
                    session=session, address_brand=address_brand
                )
                brand = Brand(
                    name=brand_n,
                    address_brand=address.id,
                )
            car.brand = brand
        else:
            setattr(car, name, value)

    await session.commit()
    await session.refresh(car)
    return car
