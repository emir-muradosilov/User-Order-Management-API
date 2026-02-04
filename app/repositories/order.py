from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert
from models.models import Order

class OrderRepositories:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order(self, id : int) -> Order:
        stmt = select(Order).where(Order.id == id)
        order = await self.db.scalar(stmt)
        return order

    async def get_order_list(self, id):
        pass

    async def delete_order(self, id):
        pass

    async def create_order(self, id):
        pass

    async def update_order(self, id):
        pass

