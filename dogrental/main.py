from fastapi import FastAPI

from . import models
from .database import engine 
from .routers import user, tenant, dog, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="dog rental API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(engine)

app.include_router(auth.router)

app.include_router(user.router)
app.include_router(tenant.router)
app.include_router(dog.router)