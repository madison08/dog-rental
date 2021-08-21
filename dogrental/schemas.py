from pydantic import BaseModel

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