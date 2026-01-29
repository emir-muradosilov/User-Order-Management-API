
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from schemas.users import UserCreate
from sqlalchemy import delete, insert, select, text

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_login(self, login:str) -> User | None:
        stmt = select(User).where(User.login == login)
        user = await self.db.scalar(stmt)
        return user

    async def create_user(self, user_date : User) -> User | None:
        self.db.add(user_date)
        await self.db.commit()
        await self.db.refresh(user_date)
        return user_date
    

    async def get_user_by_id(self, user_id) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = await self.db.scalar(stmt)
        return user
    






