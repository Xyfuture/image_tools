import asyncio


class Trigger:
    def __init__(self):
        self._lock_map = {}
        self._ret = {}

    async def wait(self, lock_id):
        assert lock_id not in self._lock_map
        self._lock_map[lock_id] = asyncio.Event()

        await self._lock_map[lock_id].wait()
        del self._lock_map[lock_id]

        ret = self._ret[lock_id]
        return ret

    async def set(self, lock_id,ret):
        # assert lock_id in self._lock_map
        if lock_id not in self._lock_map:
            return
        assert not self._lock_map[lock_id].is_set()

        self._ret[lock_id] = ret
        self._lock_map[lock_id].set()


# trigger = Trigger() # global