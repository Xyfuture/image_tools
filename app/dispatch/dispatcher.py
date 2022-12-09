import asyncio
from pydantic import BaseModel
import redis.asyncio as redis
from app.dispatch.trigger import Trigger


class DispatcherConfig(BaseModel):

    worker_stream_key:str = "Inpainting"
    worker_group_name:str = "worker"

    ack_stream_key:str = "Inpainting_finish_ack"

class Dispatcher:
    def __init__(self,worker_conn:redis.Redis,ack_conn:redis.Redis,dispatcher_config:DispatcherConfig=DispatcherConfig):
        self.config = dispatcher_config

        self.worker_conn = worker_conn
        self.ack_conn = ack_conn

        self.trigger = Trigger()

    def init_redis(self):
        pass

    async def dispatch(self,payload:dict):
        ret_id = await self.worker_conn.xadd(self.config.worker_stream_key,payload)

        ret_data = await self.trigger.wait(ret_id)

        return ret_data

    async def wait_worker_response(self):
        while True:
            payload = await self.ack_conn.xread(streams={self.config.ack_stream_key:'$'},count=1,block=0)
            tag,result = payload[0][1][0][1][b'tag'],payload[0][1][0][1][b'result']

            await self.trigger.set(tag,result)

