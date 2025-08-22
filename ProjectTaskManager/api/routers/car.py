from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.CRUD.crud_car import get_cars, get_car
from core.config import setting
from core.model import db_helper, Car
from core.schema.schema_car import CarRead

router = APIRouter(
    prefix=setting.api.v1.car,
    tags=[setting.api.v1.car_tag],
)


@router.get(
    "/",
    response_model=list[CarRead],
    status_code=status.HTTP_200_OK,
)
async def get_all_cars(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
) -> list[Car]:
    cars = await get_cars(session=session)
    return cars


@router.get(
    "/{car_id}/",
    response_model=CarRead,
    status_code=status.HTTP_200_OK,
)
async def get_car_by_id(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    car_id: UUID,
) -> Car:
    car = await get_car(session=session, car_id=car_id)
    return car
