import asyncio
import pickle
from typing import List
from loguru import logger
import redis.asyncio as redis
from fastapi import APIRouter,FastAPI, File, UploadFile
from app.dispatch.redis import conn
from app.dispatch.dispatcher import Dispatcher

inpaint_router = APIRouter()
inpaint_dispatcher = Dispatcher(conn,conn)


@inpaint_router.post("/inpaint/")
async def get_inpaint_image_mask(origin:UploadFile,mask:UploadFile):
    payload = {'image':pickle.dumps(origin.file),'mask':pickle.dumps(mask.file)}
    await inpaint_dispatcher.dispatch(payload)




