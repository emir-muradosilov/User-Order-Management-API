from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import Text, Enum, DateTime, func, ForeignKey, text
import enum
from datetime import datetime
from sqlalchemy import DateTime
from uuid import UUID, uuid4

class Base(DeclarativeBase):
    pass

'''
class Role(enum.Enum):
    admin = 'admin'
    user = 'user'
'''


class Role(Base):
    __tablename__ = 'roles'
    id :Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]=mapped_column(unique=True, nullable=False)
    description :Mapped[str] = mapped_column(nullable=True)
    is_active:Mapped[bool] = mapped_column(default=True)
    users = relationship("User", back_populates="role")
    permissions = relationship('Permission', secondary='role_permissions', back_populates='roles')

class Permission(Base):
    __tablename__='permissions'
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str]=mapped_column(unique=True, nullable=False)
    description :Mapped[str] = mapped_column(nullable=True)
    is_active:Mapped[bool] = mapped_column(default=True)
    roles= relationship('Role', secondary='role_permissions', back_populates='permissions')


class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'), primary_key=True)
    permission_id : Mapped[int] = mapped_column(ForeignKey('permissions.id'), primary_key=True)



class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    login:Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    is_active : Mapped[bool] = mapped_column(default=True)
#    role:Mapped[Role] = mapped_column(Enum(Role), default=Role.user)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    role = relationship('Role', back_populates = 'users')
    role_id : Mapped[int] = mapped_column(ForeignKey('roles.id'))




class RefreshToken(Base):
    __tablename__ = 'refresh_token'
    id : Mapped[int] = mapped_column(primary_key=True)
    jti : Mapped[UUID] = mapped_column(unique=True, index=True)
    is_revoked: Mapped[bool] = mapped_column()

    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("now() + interval '1 day'"), nullable=False)

    user_id : Mapped[int] = mapped_column(ForeignKey('users.id', ondelete = 'CASCADE'))
    user = relationship("User", back_populates="refresh_tokens")




class Order(Base):
    __tablename__='orders'
    id:Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    description : Mapped[str]=mapped_column()
    img : Mapped[str] = mapped_column()

