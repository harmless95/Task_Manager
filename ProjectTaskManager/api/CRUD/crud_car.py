from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.model import Car


async def get_cars(
    session: AsyncSession,
) -> list[Car]:
    stmt = select(Car).order_by(Car.id)
    result = await session.scalars(stmt)
    cars = result.all()
    return list(cars)
