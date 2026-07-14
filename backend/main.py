from fastapi import FastAPI

from api.routes import router
from core.init_db import initialize_database

app = FastAPI()


@app.on_event("startup")
def startup():

    initialize_database()


app.include_router(router)