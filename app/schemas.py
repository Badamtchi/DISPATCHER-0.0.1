from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class Message(BaseModel):
    title: str
    content: str

class MessageCreate(Message):
    receiver: Optional[int] = +989121143071
    seen: bool = False

class MessageEdit(Message):
    pass

class MessageBack(BaseModel):
    sender: int
    receiver: int
    title: str
    content: str
    seen: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    phone: str
    password: str
    name: Optional[str]

class UserBack(BaseModel):
    phone: str
    name: Optional[str]
    registered_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    phone: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    phone: Union[str, None] = None