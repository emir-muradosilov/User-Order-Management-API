
from models.models import Role, User
from fastapi import Depends, HTTPException, status
from core.security import get_current_user



def require_role(*roles:Role):
    async def role_checker(user:User = Depends(get_current_user)) ->User:
        if user.role not in roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Недостаточно прав')
        return user
    return role_checker
        
