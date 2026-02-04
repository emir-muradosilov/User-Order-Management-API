from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import Role

class RoleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_by_name(self, name:str) -> Role|None:
        stmt = select(Role).where(Role.name == name)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()





