from fastapi import status
from fastapi.testclient import TestClient

BASE_URL = '/api/v1/images'


def test_add_image(app, test_image):
    with TestClient(app) as client:
        r = client.post(
            url=BASE_URL,
            files={'file': test_image},
        )
        assert r.status_code == status.HTTP_201_CREATED
        assert 'image_id' in r.json()


def test_add_image_invalid_file(app, test_pdf):
    with TestClient(app) as client:
        r = client.post(
            url=BASE_URL,
            files={'file': test_pdf},
        )
        assert r.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
