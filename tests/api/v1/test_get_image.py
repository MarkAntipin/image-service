import io
from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient
from PIL import Image

BASE_URL = '/api/v1/images'


def test_get_image(app):
    w = 1000
    h = 1000
    with TestClient(app) as client:
        r = client.get(url=f'{BASE_URL}/{w}x{h}/{uuid4()}')
        assert r.status_code == status.HTTP_200_OK

        resized_image = Image.open(io.BytesIO(r.content))
        image_w, image_h = resized_image.size
        assert image_w == w
        assert image_h == h


def test_get_image_invalid_size(app):
    w = 3000
    h = 1000
    with TestClient(app) as client:
        r = client.get(url=f'{BASE_URL}/{w}x{h}/{uuid4()}')
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_image_invalid_size_step(app):
    w = 1003
    h = 1000
    with TestClient(app) as client:
        r = client.get(url=f'{BASE_URL}/{w}x{h}/{uuid4()}')
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
