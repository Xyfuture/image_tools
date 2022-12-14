import asyncio
from fastapi.testclient import TestClient
import pytest
from app.main import app

test_image_num = 1
test_image_path = r'samples/deblur/'


def test_get_image():
    with TestClient(app=app) as client:
        for i in range(test_image_num):

            response = client.get('/result/123')
            assert response.status_code == 404



