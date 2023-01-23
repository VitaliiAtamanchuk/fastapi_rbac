from typing import Any, Dict, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import EmailStr

from core.security import get_password_hash, verify_password
from core.crud import CRUDBase
from .models import User
from .schemas import UserCreate


class CRUDUser(CRUDBase[User, UserCreate, None]):
    async def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db.add(db_obj)
        await db.commit()
        # db.refresh(db_obj)
        return db_obj
    
    async def all(self, db: Session) -> list[User]:
        return await db.execute(
            select(User)
        )
    
    async def authenticate(self, db: Session, *, email: EmailStr, password: str) -> User:
        user = (await db.execute(
            select(User).where(User.email == email)
        )).scalars().first()
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        return user
    

user = CRUDUser(User)
