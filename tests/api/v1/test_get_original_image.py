from uuid import uuid4

from fastapi import status
from fastapi.testclient import TestClient

BASE_URL = '/api/v1/images'


def test_get_original_image(app):
    with TestClient(app) as client:
        r = client.get(url=f'{BASE_URL}/{uuid4()}')
        assert r.status_code == status.HTTP_200_OK


def test_get_original_image_not_found(app, mock_file_storage_image_not_found):
    with TestClient(app) as client:
        r = client.get(url=f'{BASE_URL}/{uuid4()}')
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json() == {'detail': 'Image not found'}
