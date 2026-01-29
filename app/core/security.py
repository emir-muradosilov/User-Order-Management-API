import bcrypt
from datetime import datetime, timedelta, timezone
from core.config import settings
import jwt
from fastapi import HTTPException, status, Depends
from db.db_session import async_get_db
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from repositories.refresh_token import RefreshTokenRepository
import uuid
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )

def create_access_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token:str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


def create_refresh_token(subject: str) -> dict:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    jti = str(uuid.uuid4())
    payload = {
        "sub": subject,
        "exp": expire,
        "type": "refresh",
        "jti": jti
    }
    
    response_data = {
        'token': jwt.encode(payload,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM),
        'jti': jti,
        'expires_at': expire,
    }
    return response_data


def get_current_user(token:str= Depends(oauth2_scheme), db:AsyncSession = Depends(async_get_db)):
    payload = decode_token(token)

    if payload.get('type') != 'access':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    user_id = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    try:
        user_id = int(user_id)
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid access token')
    
    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user




