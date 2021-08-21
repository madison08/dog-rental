from fastapi import FastAPI


app = FastAPI(title="dog rental API")


@app.get("/")
def index():

    return {'infos': 'welcome'}

    