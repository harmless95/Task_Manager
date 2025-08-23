from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.model import Address


async def check_address(
    session: AsyncSession,
    address_brand: dict,
):
    stmt_address = select(Address).where(
        and_(
            Address.country == address_brand.get("country"),
            Address.city == address_brand.get("city"),
            Address.street == address_brand.get("street"),
            Address.house == address_brand.get("house"),
        )
    )
    result = await session.scalars(stmt_address)
    address = result.first()
    if not address:
        address = Address(
            country=address_brand.get("country"),
            city=address_brand.get("city"),
            street=address_brand.get("street"),
            house=address_brand.get("house"),
        )
        session.add(address)
        await session.flush()
    return address
