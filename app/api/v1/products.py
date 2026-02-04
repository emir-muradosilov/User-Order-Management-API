from fastapi import APIRouter, Depends
from core.security import require_permission


router = APIRouter(prefix="/products", tags=["Products"])



@router.get("/", dependencies=[Depends(require_permission("products:read"))])
async def get_products():
    return [
        {"id": 1, "name": "Keyboard"},
        {"id": 2, "name": "Mouse"}
    ]


@router.put("/{product_id}", dependencies=[Depends(require_permission("products:update"))])
async def update_product(product_id: int):
    return {"message": f"Product {product_id} updated"}


