
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import User
from schemas.users import UserCreate, UserUpdate
from sqlalchemy import delete, insert, select, text, update

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
    

    async def delete_user(self, user_id):
        stmt = update(User).where(User.id == user_id).values(is_active = False).returning(User)
        user = await self.db.execute(stmt)
        await self.db.commit()
        return user.scalar_one_or_none()

    async def get_user_by_id(self, user_id) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = await self.db.scalar(stmt)
        return user
    

    async def update_user_data(self, user_id:int, data:UserUpdate) -> User|None:

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            return await self.db.get(User, user_id)
        
        stmt = update(User).where(User.id == user_id).values(**update_data).returning(User)
        result = await self.db.execute(stmt)
        await self.db.commit()
        return result.scalar_one_or_none()






