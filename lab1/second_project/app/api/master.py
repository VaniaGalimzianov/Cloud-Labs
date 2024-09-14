from fastapi import APIRouter


master = APIRouter()


@master.get('/')
async def index():
    return {"Project_name": "SECOND"}
