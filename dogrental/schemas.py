from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    firstname: str
    lastname: str
    username: str
    email: str
    password: str


    class Config():
        orm_mode = True

class Tenant(BaseModel):
    
    firstname: str
    lastname: str
    email: str
    adress: str

class Dog(BaseModel):
    name: str
    race: str


class Login(BaseModel):

    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None