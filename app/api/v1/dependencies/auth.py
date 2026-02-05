from fastapi import Depends, HTTPException, status
from repositories.user import UserRepository
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_session import async_get_db
from core.security import decode_token
from models.models import User

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(async_get_db)
        ) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    user_id : str | None = payload.get('sub')
    token_type : str | None = payload.get('type')

    if user_id is None or token_type != 'access':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    repo = UserRepository(db)
    user = await repo.get_user_by_id(int(user_id))

    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User nor found")
    
    return user
