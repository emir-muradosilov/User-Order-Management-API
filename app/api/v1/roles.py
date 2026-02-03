from fastapi import APIRouter, Depends
from core.security import require_permission




router = APIRouter(prefix='', tags=[''])



@router.post("/", dependencies=[Depends(require_permission("roles:update"))])
async def create_role():
    return {"message": "role created"}






