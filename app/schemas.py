from typing import Optional
from pydantic import BaseModel, EmailStr

class UserResponse(BaseModel):
    email: EmailStr

class Post(BaseModel):
    title: str 
    content:str
    published: bool=True

class User(BaseModel):
    email:EmailStr
    password: str

    class Config:
        orm_mode=True

class Login(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str 

class TokenData(BaseModel):
    id: Optional[str]=None
