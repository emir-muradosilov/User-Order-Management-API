from fastapi import APIRouter
from schemas.users import UserResponse, UserCreate, UserLogin
from repositories.user import UserRepository
from repositories.refresh_token import RefreshTokenRepository
from services.auth import AuthService
from fastapi import Depends
from db.db_session import async_get_db
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.auth import RefreshTokenRequest, TokenResponse
from schemas.logout import LogoutRequest

router = APIRouter(prefix= "/auth", tags=['Auth'])


@router.post('/register', response_model=UserResponse)
async def registration(
    data: UserCreate,
    session: AsyncSession = Depends(async_get_db),
):

    repo = UserRepository(session)
    service = AuthService(repo)
    return await service.user_registration(data)



@router.post('/login', response_model=TokenResponse)
async def login(data:UserLogin, session: AsyncSession = Depends(async_get_db)):

    repo = UserRepository(session)
    service = AuthService(repo)
    return await service.user_login(data)


@router.post('/refresh', response_model=TokenResponse)
async def refresh(data:RefreshTokenRequest, session: AsyncSession = Depends(async_get_db)):

    repo = UserRepository(session)
    service = AuthService(repo)
    return await service.refresh_access_token(data.refresh_token)


@router.post('/logout', status_code=204)
async def logout(data:LogoutRequest, session: AsyncSession = Depends(async_get_db)):
#    repo = UserRepository(session)
    refresh_repo = RefreshTokenRepository(session)
    service = AuthService(None, refresh_repo)
    await service.logout(data.refresh_token)


