
from fastapi import HTTPException, status
from schemas.orders import OrderUpdate, OrderCreate, OrderResponse, OrderListResponse
from repositories.order import OrderRepositories


class Orders:

    def __init__(self, repo:OrderRepositories):
        self.repo = repo

    async def get_order(self, id:int) -> OrderResponse:
        order = self.repo.get_order(id)
        if not order:
            raise HTTPException(self, status_code=status.HTTP_400_BAD_REQUEST, detail='Order не найден')
        return order

    async def get_order_list(self, list:list[int]) -> OrderListResponse:
        order_list = self.repo.get_order_list(list)
        if not order_list:
            raise HTTPException(self, status_code=status.HTTP_400_BAD_REQUEST, detail='Order не найден')
        return order_list
    
    async def create_order(self, date:OrderCreate) -> OrderResponse:
        pass

    async def update_order(self, date:OrderUpdate) -> OrderResponse:
        pass
    
    async def delete_order(self, id:int) -> bool:
        pass




