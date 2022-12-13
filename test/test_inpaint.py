import asyncio
from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from app.main import app

# client = TestClient(app)

test_image_num = 1
test_image_path = r'D:\code\swdesign\image_tools\test\samples\inpaint\\'


# @pytest.mark.anyio
# async def test_inpaint():
#     # await asyncio.gather(app.router.startup())
#     async with AsyncClient(app=app,base_url='http://localhost',) as client:
#         # await asyncio.sleep(10)
#         asyncio.create_task(app.router.startup())
#         for i in range(test_image_num):
#             file = {
#                 'origin': open(test_image_path + f'origin_{i}.png', 'rb'),
#                 'mask': open(test_image_path + f'mask_{i}.png', 'rb')
#             }
#             print('here')
#             response = await client.post('/inpaint', files=file)
#             assert response.status_code == 200


def test_inpaint():
    with TestClient(app=app) as client:
        for i in range(test_image_num):
            file = {
                'origin': open(test_image_path + f'origin_{i}.png', 'rb'),
                'mask': open(test_image_path + f'mask_{i}.png', 'rb')
            }
            print('here')
            response = client.post('/inpaint', files=file)
            assert response.status_code == 200
            url = response.json()['image_url']
            print(url)

