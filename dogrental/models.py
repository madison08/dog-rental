from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String)

    tenants = relationship("Tenant", back_populates="creator")

class Dog(Base):

    __tablename__ = 'dogs'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    race = Column(String, default="unknown")

    tenant_id = Column(Integer, ForeignKey('tenants.id'))

    owner = relationship("Tenant", back_populates="dogs")

class Tenant(Base):

    __tablename__ = 'tenants'

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    adress = Column(String)

    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User", back_populates="tenants")

    dogs = relationship("Dog", back_populates="owner")

