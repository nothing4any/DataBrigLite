from fastapi import APIRouter

from business.service import userservice
from schemas import schemas
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger("user")

server = userservice.Service()


@router.post("/create")
async def user_create(user: schemas.UserCreate):
    res = await server.user_create(user)
    return res


@router.post("/")
async def users(item: schemas.UserSearch):
    res = await server.user_list(item)
    return res


@router.post("/update")
async def user_update(item: schemas.UserUpdate):
    res = await server.user_update(item)
    return res


@router.post("/delete")
async def user_update(item: schemas.UserDelete):
    res = await server.user_delete(item)
    return res

@router.post("/getusermap")
async def user_map_req():
    res = await server.user_map_req()
    return res