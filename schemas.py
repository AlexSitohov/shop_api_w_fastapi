from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str
    price: int

    class Config:
        orm_mode = True


class Customer(BaseModel):
    name: str
    password: str
    balance: int

    class Config:
        orm_mode = True


class CustomerResponse(BaseModel):
    id: int
    name: str
    balance: int

    class Config:
        orm_mode = True


class Order(BaseModel):
    # customer_id: int
    items_id: list[int]


class OrderResponse(BaseModel):
    id: int
    date_time_created: datetime
    customer: CustomerResponse
    items: list[Item]

    class Config:
        orm_mode = True


class Login(BaseModel):
    name: str
    password: str


class TokenData(BaseModel):
    id_customer: int
    name_customer: str
    is_staff: bool


class Rate(BaseModel):
    item_id: int
    ball: int = Field(gt=0, lt=6)

    class Config:
        orm_mode = True
