from fastapi import APIRouter

from .car import router as router_car

all_routers = APIRouter()

all_routers.include_router(router=router_car)
