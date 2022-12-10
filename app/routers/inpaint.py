import asyncio
import pickle
from typing import List
from loguru import logger
import redis.asyncio as redis
from fastapi import APIRouter,FastAPI, File, UploadFile
from app.redis import conn
from app.dispatch.dispatcher import Dispatcher
from app.container import dispatcher_list

inpaint_router = APIRouter()
inpaint_dispatcher = Dispatcher(conn,conn,conn)
dispatcher_list.append(inpaint_dispatcher)

@inpaint_router.post("/inpaint")
async def get_inpaint_image_mask(origin:UploadFile,mask:UploadFile):
    payload = {'image':pickle.dumps(origin.file.read()),'mask':pickle.dumps(mask.file.read())}
    result_url = await inpaint_dispatcher.dispatch(payload)
    return {"image_url":"http://localhost:5003"+result_url}




