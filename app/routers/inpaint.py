import asyncio
import pickle
from typing import List
from loguru import logger
import redis.asyncio as redis
from fastapi import APIRouter, FastAPI, File, UploadFile
from app.redis import conn
from app.dispatch.dispatcher import Dispatcher, DispatcherConfig
from app.container import dispatcher_list

inpaint_dispatcher_config = DispatcherConfig(
    worker_name="Inpainting",
    worker_stream_key="Inpainting_worker",
    worker_group_name="worker",
    ack_stream_key="Inpainting_finish_ack",
    ack_group_name="master"
)

inpaint_router = APIRouter()
inpaint_dispatcher = Dispatcher(conn, conn, conn, inpaint_dispatcher_config)
dispatcher_list.append(inpaint_dispatcher)


@inpaint_router.post("/inpaint")
async def get_inpaint_image_mask(origin: UploadFile, mask: UploadFile):
    payload = {'image': pickle.dumps(origin.file.read()), 'mask': pickle.dumps(mask.file.read())}
    result_url = await inpaint_dispatcher.dispatch(payload)
    if result_url == '/result/error':
        return {"status": 0, 'error': 'inference failed'}
    # return {"image_url":"http://localhost:5003"+result_url}
    return {"image_url": result_url}
