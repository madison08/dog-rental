from fastapi import FastAPI

from . import models
from .database import engine 
from .routers import user, tenant, dog

app = FastAPI(title="dog rental API")


models.Base.metadata.create_all(engine)


app.include_router(user.router)
app.include_router(tenant.router)
app.include_router(dog.router)