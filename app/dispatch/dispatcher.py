import asyncio

from loguru import logger
from pydantic import BaseModel
import redis.asyncio as redis
from app.dispatch.trigger import Trigger


class DispatcherConfig(BaseModel):
    worker_name = "Inpainting"

    worker_stream_key: str = "Inpainting_worker"
    worker_group_name: str = "worker"

    ack_stream_key: str = "Inpainting_finish_ack"
    ack_group_name: str = "master"


class Dispatcher:
    def __init__(self, worker_conn: redis.Redis, ack_conn: redis.Redis, buffer_conn: redis.Redis
                 , dispatcher_config: DispatcherConfig = DispatcherConfig()):
        self.config = dispatcher_config

        self.worker_conn = worker_conn
        self.ack_conn = ack_conn
        self.buffer_conn = buffer_conn

        self.trigger = Trigger()

        # asyncio.run(self.init_redis())

    async def init_redis(self):
        try:
            ret = await self.worker_conn.xinfo_groups(self.config.worker_stream_key)
            is_in = False
            for group in ret:
                if self.config.worker_group_name == group['name'].decode('utf-8'):
                    is_in = True
                    break
            if not is_in:
                await self.worker_conn.xgroup_create(name=self.config.worker_stream_key,
                                                     groupname=self.config.worker_group_name,
                                                     id='$', mkstream=False)
        except:
            await self.worker_conn.xgroup_create(name=self.config.worker_stream_key,
                                                 groupname=self.config.worker_group_name,
                                                 id='$', mkstream=True)

        try:
            ret = await self.ack_conn.xinfo_groups(self.config.ack_stream_key)
            is_in = False
            for group in ret:
                if self.config.ack_group_name == group['name'].decode('utf-8'):
                    is_in = True
                    break
            if not is_in:
                await self.ack_conn.xgroup_create(name=self.config.ack_stream_key,
                                                  groupname=self.config.ack_group_name,
                                                  id='$', mkstream=False)
        except:
            await self.ack_conn.xgroup_create(name=self.config.ack_stream_key,
                                              groupname=self.config.ack_group_name,
                                              id='$', mkstream=True)

    async def dispatch(self, payload: dict):
        lock_id = await self.worker_conn.xadd(self.config.worker_stream_key, payload)

        result_url = await self.trigger.wait(lock_id)

        return result_url

    async def wait_worker_response(self):
        await self.init_redis()
        # logger.info('waiting')
        while True:
            payload = await self.ack_conn.xreadgroup(groupname=self.config.ack_group_name, consumername='master',
                                                     streams={self.config.ack_stream_key: '>'}, block=0, count=1)
            tag,status, result = payload[0][1][0][1][b'tag'],payload[0][1][0][1][b'status'],payload[0][1][0][1][b'result']
            if status == b'ok':
                result_url = await self.add_result_to_buffer(tag, result)
                await self.trigger.set(tag, result_url)
            else :
                await self.trigger.set(tag,'/result/error')

    async def add_result_to_buffer(self, key, value):
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        await self.buffer_conn.set(key, value)
        return '/result/{}'.format(key)
