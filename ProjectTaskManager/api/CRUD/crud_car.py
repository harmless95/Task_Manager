from uuid import UUID
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select
from fastapi import HTTPException, status

from api.CRUD.crud_address import check_address
from core.model import Car, Brand, Address
from core.schema.schema_car import CarUpdate, CarCreate

log = logging.getLogger(__name__)


async def create_car(
    session: AsyncSession,
    data_car: CarCreate,
) -> Car:
    stmt = select(Car).where(Car.name == data_car.name)
    result = await session.scalars(stmt)
    car = result.first()
    if car:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"nvalid such a {data_car.name} already exists",
        )
    stmt_brand = select(Brand).where(Brand.name == data_car.brand_id.name)
    result = await session.scalars(stmt_brand)
    brand = result.first()
    if not brand:
        brand = Brand(name=data_car.brand_id.name)
        session.add(brand)
        await session.flush()
        address_brand = data_car.brand_id.address
        address = Address(
            country=address_brand.country,
            city=address_brand.city,
            street=address_brand.street,
            house=address_brand.house,
            brand_id=brand.id,
        )
        session.add(address)
        await session.flush()

    car = Car(
        name=data_car.name,
        color=data_car.color,
        price=data_car.price,
        brand_id=brand.id,
    )
    session.add(car)
    await session.commit()
    stmt = (
        select(Car)
        .options(selectinload(Car.brand).selectinload(Brand.addresses))
        .where(Car.id == car.id)
    )
    result_new = await session.scalars(stmt)
    car = result_new.first()
    await session.refresh(car)
    return car


async def get_cars(
    session: AsyncSession,
) -> list[Car]:
    stmt = select(Car).order_by(Car.id)
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
