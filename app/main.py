import io
import pickle
import asyncio
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
import fastapi
from starlette.middleware.cors import CORSMiddleware

from app.redis import conn
from app.container import dispatcher_list
import app.routers.inpaint as inpaint
import app.routers.deblur as deblur

app = fastapi.FastAPI()


@app.on_event('startup')
def register_dispatcher_listener():
    for dispatcher in dispatcher_list:
        asyncio.create_task(dispatcher.wait_worker_response())

origins= [
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5003",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],
)

app.include_router(inpaint.inpaint_router)
app.include_router(deblur.deblur_router)


@app.get('/result/{image_key}')
async def get_result(image_key: str):
    if image_key == 'error':
        return StreamingResponse(open('app/statics/failed.jpg','rb'),media_type='image/jpeg')
    img_byte = await conn.get(image_key)
    if img_byte:
        img_byte = pickle.loads(img_byte)
        img_file = io.BytesIO(img_byte)
        return StreamingResponse(img_file, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Item not found")
