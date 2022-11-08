from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture


@pytest.fixture()
def mock_env(monkeypatch: MonkeyPatch):
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'AWS_ACCESS_KEY_ID')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'AWS_SECRET_ACCESS_KEY')
    monkeypatch.setenv('REGION_NAME', 'REGION_NAME')
    monkeypatch.setenv('BUCKET', 'BUCKET')


@pytest.fixture()
def mock_s3_client(mocker: MockerFixture, test_image_bytes) -> None:
    mocker.patch('src.dal.file_storage.s3.S3FileStorage.set')
    mocker.patch('src.dal.file_storage.s3.S3FileStorage.get', return_value=test_image_bytes)


@pytest.fixture()
def mock_s3_client_image_not_found(mocker: MockerFixture, test_image_bytes) -> None:
    mocker.patch('src.dal.file_storage.s3.S3FileStorage.get', return_value=None)


@pytest.fixture()
def app(mock_env, mock_s3_client):
    from api.app import create_app
    app = create_app()
    return app


@pytest.fixture()
def test_data_path() -> Path:
    from settings import BASE_DIR
    return Path(BASE_DIR, 'tests', 'data')


@pytest.fixture()
def image_path(test_data_path) -> Path:
    return Path(test_data_path, 'test.jpg')


@pytest.fixture(scope='function')
def test_image_bytes(image_path) -> bytes:
    with open(image_path, 'rb') as f:
        yield f.read()


@pytest.fixture(scope='function')
def test_image(image_path) -> bytes:
    with open(image_path, 'rb') as f:
        yield "test.jpg", f, "image/jpg"


@pytest.fixture(scope='function')
def test_pdf(image_path) -> bytes:
    with open(image_path, 'rb') as f:
        yield "test.pdf", f, "application/pdf"
