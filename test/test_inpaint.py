import asyncio
from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient
from app.main import app

# client = TestClient(app)

test_image_num = 1
test_image_path = r'samples/inpaint/'


def test_inpaint():
    with TestClient(app=app) as client:
        for i in range(test_image_num):
            file = {
                'origin': open(test_image_path + f'origin_{i}.png', 'rb'),
                'mask': open(test_image_path + f'mask_{i}.png', 'rb')
            }

            response = client.post('/inpaint', files=file)
            assert response.status_code == 200
            assert response.json()['image_url']

