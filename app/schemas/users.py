from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from datetime import date
from datetime import datetime

class Role(str, Enum):
    admin : str = 'admin'
    user: str = 'user'

class UserCreate(BaseModel):
    name :str
    login :str
    email : EmailStr
    password : str
#    is_active : bool
#    role : Role = Field(default=Role.user)


class UserResponse(BaseModel):
    name :str
    login :str
    email : EmailStr
    is_active : bool
#    role : str
#    created_at : datetime


class UserUpdate(BaseModel):
    name :str
    email : None | EmailStr



class UserLogin(BaseModel):
    login :str
    password: str


