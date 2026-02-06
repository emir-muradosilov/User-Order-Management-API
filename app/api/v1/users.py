from fastapi import APIRouter, Depends, Response, Cookie, HTTPException
from api.v1.dependencies.auth import get_current_user
from models.models import User
from core.security import require_permission
from typing import Annotated
from settings import REFRESH_COOKIE_NAME, REFRESH_COOKIE_PATH,REFRESH_COOKIE_SAMESITE,REFRESH_COOKIE_SECURE
from repositories.refresh_token import RefreshTokenRepository
from services.auth import AuthService

from schemas.users import UserResponse, UserUpdate
from repositories.user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_session import async_get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "login": current_user.login,
        "email": current_user.email,
#        "role": current_user.role,
    }


@router.get("/", dependencies=[Depends(require_permission("users:read"))]
)
async def get_users():
    return {"message": "users list"}


@router.patch('/me', response_model=UserResponse)
async def update_user_data(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(async_get_db),
):
    user_repo = UserRepository(session)
    user = await user_repo.update_user_data(
        user_id=current_user.id,
        data=data
    )
    return user


@router.post('delete')
async def delete_user(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(async_get_db)
):

    user_repo = UserRepository(session)
    
    user = await user_repo.delete_user(user_id=current_user.id) 

    return {"message": "Your account is deleted", 'user status': user.is_active}