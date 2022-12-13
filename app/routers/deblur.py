import asyncio
import pickle
from typing import List
from loguru import logger
import redis.asyncio as redis
from fastapi import APIRouter, FastAPI, File, UploadFile
from app.redis import conn
from app.dispatch.dispatcher import Dispatcher, DispatcherConfig
from app.container import dispatcher_list


deblur_dispatcher_config = DispatcherConfig(
    worker_name = "Deblur",
    worker_stream_key= "Deblur_worker",
    worker_group_name = "worker",
    ack_stream_key = "Deblur_finish_ack",
    ack_group_name = "master"
)


deblur_router = APIRouter()
deblur_dispatcher = Dispatcher(conn, conn, conn,deblur_dispatcher_config)
dispatcher_list.append(deblur_dispatcher)


@deblur_router.post("/deblur")
async def get_deblur_origin_image(origin: UploadFile):
    payload = {'image': pickle.dumps(origin.file.read())}
    result_url = await deblur_dispatcher.dispatch(payload)
    return {"image_url": "http://localhost:5003" + result_url}
