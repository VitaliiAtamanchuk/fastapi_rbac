from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from core import security
from core.deps import get_db
from core.config import settings
from . import crud, models


auth_scheme = HTTPBearer()
# class TokenBearer:
#     async def __call__(self, request: Request) -> str:
#         authorization = request.headers.get("Authorization")
#         scheme, param = get_authorization_scheme_param(authorization)
#         if not authorization or scheme.lower() != "bearer":
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Not authenticated",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return param


async def get_current_active_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        sub = payload['sub']
    except (jwt.JWTError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await crud.user.get(db, id=sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_admin(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


def get_current_active_role(role: models.User.Roles):
    def func(
        current_user: models.User = Depends(get_current_active_user),
    ) -> models.User:
        if current_user.role != role:
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )
        return current_user
    return func


get_current_active_role1 = get_current_active_role(models.User.Roles.role1)
get_current_active_role2 = get_current_active_role(models.User.Roles.role2)
get_current_active_role3 = get_current_active_role(models.User.Roles.role3)
