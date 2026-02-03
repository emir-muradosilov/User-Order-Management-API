from fastapi import APIRouter, Depends
from api.v1.dependencies.auth import get_current_user
from models.models import User
from core.security import require_permission



router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):

    return {
        "id": current_user.id,
        "login": current_user.login,
        "email": current_user.email,
        "role": current_user.role,
    }


@router.get("/", dependencies=[Depends(require_permission("users:read"))]
)
async def get_users():
    return {"message": "users list"}


