from fastapi import FastAPI

from . import models
from .database import engine 

app = FastAPI(title="dog rental API")


models.Base.metadata.create_all(engine)


@app.get("/")
def index():

    return {'infos': 'welcome'}

