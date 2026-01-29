

from sqlalchemy.ext.asyncio import AsyncSession
from models.models import RefreshToken, User
from sqlalchemy import insert, select, delete
from fastapi import HTTPException, status

class RefreshTokenRepository:


    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def save_refresh_token(self, user_data:User, jti: str)-> RefreshToken | None :
        try:
            refresh_token = RefreshToken(
                jti = jti,
                is_revoked = False,
                user_id = user_data.id,
            )
            await self.db.add(refresh_token)
            await self.db.commit()
            return await self.db.refresh(refresh_token)
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Ошибка при работе с Refresh Token: {e}')
        

    async def select_refresh_token_by_jti(self, jti:str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.jti==jti, RefreshToken.is_revoked == False)
        refresh_token = await self.db.scalar(stmt)
        return refresh_token


    async def revoke_refresh_token(self, jti:str) -> bool:
        refresh_token = await self.select_refresh_token_by_jti(jti)
        if not refresh_token:
            return False
        
        refresh_token.is_revoked = True
        await self.db.commit()
        return True
    

    async def return_refresh_token_by_user_id(self, user_id:int) -> RefreshToken:
        stmt = select(RefreshToken).where(RefreshToken.user_id==user_id, RefreshToken.is_revoked == False)
        refresh_token = await self.db.scalar(stmt)
        return refresh_token