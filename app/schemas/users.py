from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import date
from datetime import datetime

class Role(str, Enum):
    admin : str = 'admin'
    user: str = 'user'

class UserCreate(BaseModel):
    login :str
    email : EmailStr
    password : str
    is_active : bool
    role : Role = Field(default=Role.user)


class UserResponse(BaseModel):
    login :str
    email : EmailStr
    is_active : bool
    role : Role
    created_at : datetime


class UserUpdate(BaseModel):
    email : None | EmailStr
    password_hash : None | str
    is_active : None | bool


class UserLogin(BaseModel):
    login :str
    password: str


