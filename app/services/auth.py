from fastapi import HTTPException, status
import bcrypt
from sqlalchemy import select
from models.models import User
from db.db_session import async_get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from repositories.refresh_token import RefreshTokenRepository
from schemas.users import UserCreate, UserLogin
from core.security import hash_password, verify_password, create_access_token, create_refresh_token

import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from repositories.role import  RoleRepository
from core.security import decode_token

class AuthService:

    def __init__(self, repo : UserRepository | None, refresh:RefreshTokenRepository | None = None, role_repo : RoleRepository | None = None):
        self.repo = repo
        self.refresh = refresh
        self.role_repo = role_repo
    

    async def user_registration(self, data: UserCreate) -> User:
        existing_user = await self.repo.get_user_by_login(data.login)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Данный пользователь уже существует'
                )
        
        role = await self.role_repo.get_by_name("user")
        if not role:
            raise RuntimeError("Default role 'user' not found")

        user = User(
            login = data.login,
            email = data.email,
            password_hash = hash_password(data.password),
            is_active = True,
            role = role
        )
        
        user = await self.repo.create_user(user)
        
        return {
        "login": user.login,
        "email": user.email,
        "is_active": user.is_active,
        "role": role.name,
        "created_at": user.created_at,
    }


    async def user_login(self, data: UserLogin):
        user = await self.repo.get_user_by_login(data.login)
        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        
            
        token_data  = create_refresh_token(str(user.id))

        return {
        "access_token": create_access_token(str(user.id)),
        "refresh_token": token_data['token'],
        "refresh_jti": token_data['jti'],
        "refresh_expires": token_data["expires_at"]
        }

        
    async def refresh_access_token(self, refresh_token:str):
        
        payload = decode_token(refresh_token)

        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
        
        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        user = await self.repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")
        
        jti = payload.get('jti')
        refresh_token = await self.refresh.select_refresh_token_by_jti(jti)

        if not jti or not refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        is_expired = refresh_token.expires_at < datetime.now(timezone.utc)

        if refresh_token.is_revoked or is_expired:
            if refresh_token.is_revoked:
                await self.refresh.revoke_refresh_token(jti)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or revoked")


        response_data = create_refresh_token(str(user.id))
        await self.refresh.save_refresh_token(user, response_data["jti"])

        return {
            "access_token": create_access_token(str(user.id)),
            "refresh_token": response_data['token'],
            "token_type": "bearer"
        }


    async def logout(self, refresh_token : str) -> None:
        
        payload = decode_token(refresh_token)

        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not a refresh token")

        jti = payload.get('jti')
        if not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

        db_token = await self.refresh.select_refresh_token_by_jti(jti)
        if not db_token or db_token.is_revoked:
            return 
        
        await self.refresh.revoke_refresh_token(jti)


