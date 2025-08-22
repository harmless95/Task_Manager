from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from fastapi import HTTPException, status

from core.model import Car


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
