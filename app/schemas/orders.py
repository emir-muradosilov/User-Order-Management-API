
from pydantic import BaseModel



class OrderCreate(BaseModel):
    name: str
    description: str
    img: bytes


class OrderUpdate(BaseModel):
    name: str
    description: str
    img: bytes


class OrderResponse(BaseModel):
    name: str
    description: str
    img: str

class OrderListResponse(BaseModel):
    name: str
    description: str
    img: str
