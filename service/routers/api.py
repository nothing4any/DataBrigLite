from fastapi import APIRouter

from business.service import apiservice
from schemas.schemas import *
from utils.logger import setup_logger

router = APIRouter()
logger = setup_logger("api")

server = apiservice.Service()


@router.post("/login")
async def login(item: Login):
    res = await server.login(item)
    return res


@router.post("/unlogin")
async def unlogin(item: Token):
    res = await server.unlogin(item)
    return res
