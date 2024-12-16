from fastapi import FastAPI
from . import Controller

app = FastAPI()

app.include_router(Controller.router)
