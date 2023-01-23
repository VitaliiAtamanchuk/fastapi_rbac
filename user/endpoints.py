from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr

from core import deps, security
from core.config import settings
from . import schemas, crud, models
from .deps import get_current_active_user, get_current_active_admin, get_current_active_role

router = APIRouter()


@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
):
    try:
        user = await crud.user.create(db, obj_in=user_in)
    except IntegrityError:
        return HTTPException(status_code=400, detail="Email already in use")
    return user


@router.get("/")
async def list_users(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(get_current_active_admin)
):
    users = await crud.user.all(db)
    return users.scalars().all()


@router.post("/auth")
async def login_user(
    db: Session = Depends(deps.get_db),
    email: EmailStr = Body(),
    password: str = Body(),
):
    user = await crud.user.authenticate(
        db, email=email, password=password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return {
        "token": security.create_access_token(user.id)
    }


@router.get("/test-login")
async def login_test(
    current_user: models.User = Depends(get_current_active_user)
):
    return current_user

@router.get("/test-role")
async def login_test(
    current_user: models.User = Depends(get_current_active_role(models.User.Roles.role2))
):
    return current_user
