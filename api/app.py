from logging import getLogger

import aioboto3
from backend_utils.server import register_routers
from fastapi import FastAPI

from api.routes.v1.app import v1_routers
from settings import IMAGES_DIR, S3Settings, Storage, app_settings
from src.dal.file_storage.disk import DiskFileStorage
from src.dal.file_storage.s3 import S3FileStorage

logging = getLogger(__name__)


def setup_s3_storage(app: FastAPI):
    s3_settings = S3Settings()
    app.state.s3_session = aioboto3.Session(
        aws_access_key_id=s3_settings.ACCESS_KEY_ID,
        aws_secret_access_key=s3_settings.SECRET_ACCESS_KEY,
        region_name=s3_settings.REGION_NAME
    )
    app.state.file_storage = S3FileStorage(
        session=app.state.s3_session,
        bucket=s3_settings.BUCKET,
        endpoint_url=s3_settings.ENDPOINT_URL
    )


def setup_disk_storage(app: FastAPI):
    app.state.file_storage = DiskFileStorage(images_dir=IMAGES_DIR)


def setup_storage(app: FastAPI):
    if app_settings.STORAGE == Storage.s3:
        setup_s3_storage(app)
    elif app_settings.STORAGE == Storage.disk:
        setup_disk_storage(app)
    else:
        raise ValueError('provided invalid storage type')


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.TITLE,
        version=app_settings.VERSION,
    )
    setup_storage(app)
    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    return app
