from fastapi import APIRouter, Response, Cookie, HTTPException
from schemas.users import UserResponse, UserCreate, UserLogin, UserUpdate
from repositories.user import UserRepository
from repositories.refresh_token import RefreshTokenRepository
from services.auth import AuthService
from fastapi import Depends
from db.db_session import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import RefreshTokenRequest, TokenResponse
from schemas.logout import LogoutRequest
from fastapi.responses import JSONResponse
from typing import Annotated
from settings import REFRESH_COOKIE_NAME, REFRESH_COOKIE_PATH,REFRESH_COOKIE_SAMESITE,REFRESH_COOKIE_SECURE
from datetime import datetime
from repositories.role import RoleRepository
from api.v1.dependencies.auth import get_current_user


router = APIRouter(prefix= "/auth", tags=['Auth'])


@router.post('/register', response_model=UserResponse)
async def registration(
    data: UserCreate,
    session: AsyncSession = Depends(async_get_db),
):

    repo = UserRepository(session)
    role_repo = RoleRepository(session)

    service = AuthService(repo = repo, role_repo=role_repo)

    return await service.user_registration(data)



@router.post('/login', response_model=TokenResponse)
async def login(data:UserLogin, response: Response, session: AsyncSession = Depends(async_get_db) ):

    user_repo = UserRepository(session)
    refresh_repo = RefreshTokenRepository(session)

    service = AuthService(user_repo, refresh_repo)

    tokens = await service.user_login(data)

    response.set_cookie(
        key = REFRESH_COOKIE_NAME,
        value = tokens['refresh_token'],
        httponly=True,
        secure= REFRESH_COOKIE_SECURE,
        path = REFRESH_COOKIE_PATH,
        )
    
    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
        }


@router.post('/refresh', response_model=TokenResponse)
async def refresh(response: Response, refresh_token: Annotated[str | None, Cookie()] = None, session: AsyncSession = Depends(async_get_db)):

    service = AuthService(repo=UserRepository(session), refresh=RefreshTokenRepository(session))
    tokens = await service.refresh_access_token(refresh_token)

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    response.set_cookie(
    key = REFRESH_COOKIE_NAME,
    value = tokens['refresh_token'],
    httponly=True,
    secure= REFRESH_COOKIE_SECURE,
    path = REFRESH_COOKIE_PATH,
    )
    
    return {
        "access_token": tokens["access_token"],
        "token_type": "bearer",
        }


@router.post('/logout', status_code=204)
async def logout():
    return {"message": "Logged out"}


'''
@router.post('/logout', status_code=204)
async def logout(
    response: Response,
    refresh_token: Annotated[str | None, Cookie()] = None,
    session: AsyncSession = Depends(async_get_db)
    ):
    
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")


    service = AuthService(repo = None,  refresh=RefreshTokenRepository(session))

    await service.logout(refresh_token)

    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path=REFRESH_COOKIE_PATH,
        )
'''



    