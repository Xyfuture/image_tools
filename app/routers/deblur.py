import asyncio
import pickle
from typing import List
from loguru import logger
import redis.asyncio as redis
from fastapi import APIRouter,FastAPI, File, UploadFile
from app.redis import conn
from app.dispatch.dispatcher import Dispatcher
from app.container import dispatcher_list

deblur_router = APIRouter()
deblur_dispatcher = Dispatcher(conn,conn,conn)
dispatcher_list.append(deblur_dispatcher)

@deblur_router.post("/deblur")
async def get_inpaint_image_mask(origin:UploadFile):
    payload = {'image':pickle.dumps(origin.file.read())}
    result_url = await deblur_dispatcher.dispatch(payload)
    return {"image_url":"http://localhost:5003"+result_url}




