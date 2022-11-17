from logging import getLogger

import aioboto3
from backend_utils.server import register_routers
from fastapi import FastAPI

from api.routes.v1.app import v1_routers
from settings import S3Settings, app_settings
from src.dal.file_storage.s3 import S3FileStorage

logging = getLogger(__name__)


def setup_s3_storage(app: FastAPI):
    s3_settings = S3Settings()
    app.state.s3_session = aioboto3.Session(
        aws_access_key_id=s3_settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=s3_settings.AWS_SECRET_ACCESS_KEY,
        region_name=s3_settings.REGION_NAME
    )
    app.state.file_storage = S3FileStorage(session=app.state.s3_session, bucket=s3_settings.BUCKET)


def create_app() -> FastAPI:
    app = FastAPI(
        title=app_settings.TITLE,
        version=app_settings.VERSION,
    )
    setup_s3_storage(app)
    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    return app
