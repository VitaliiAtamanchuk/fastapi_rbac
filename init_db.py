import asyncio


from core.database import SessionLocal
from core.security import get_password_hash
from user.models import User


async def main():
    async with SessionLocal() as db:
        db_obj = User(
            email='admin@example.com',
            password=get_password_hash('admin'),
            full_name='Admin',
            is_active=True,
            is_admin=True,
        )
        db.add(db_obj)
        await db.commit()


if __name__ == "__main__":
    asyncio.run(main())
