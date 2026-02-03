
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.models import Permission, User, Role, RolePermission

class PermissionRepository:

    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_permission_by_role_id(self, role_id:int) -> set[str]:
#        stmt = select(RolePermission).where(Role.permissions == role_id)
        stmt = (select(Permission.name).join(RolePermission, RolePermission.permission_id == Permission.id).where(RolePermission.role_id == role_id))
        permissions = await self.session.execute(stmt)
        return {row[0] for row in permissions.all()}



