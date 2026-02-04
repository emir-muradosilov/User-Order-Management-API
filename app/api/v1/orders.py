
from fastapi import APIRouter, dependencies, Depends
from schemas.orders import OrderCreate
from core.security import require_permission


router = APIRouter(prefix='/orders', tags=['Orders'])



@router.get('/orders', dependencies=[Depends(require_permission("orders:read"))])
async def get_orders():
    return [
        {"id": 1, "item": "Laptop"},
        {"id": 2, "item": "Phone"}
    ]

@router.post('/orders', dependencies=[Depends(require_permission("orders:write"))])
async def create_orders(order: OrderCreate):
    return {"message": "Order created"}

@router.delete('/{order_id}', dependencies=[Depends(require_permission("orders:write"))])
async def delete_orders(order_id: int):
    return {"message": f"Order {order_id} deleted"}





