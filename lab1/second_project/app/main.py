from fastapi import FastAPI

from app.api.master import master

app = FastAPI()

app.include_router(master)
