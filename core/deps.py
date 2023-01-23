from typing import Generator

from core.database import SessionLocal


async def get_db() -> Generator:
    async with SessionLocal() as db:
        yield db