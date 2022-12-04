from concurrent.futures import ProcessPoolExecutor

import aioboto3
from backend_utils.server import register_routers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.middlewares.errors import ErrorsMiddleware
from api.middlewares.logging import LoggingMiddleware
from api.routes.v1.app import v1_routers
from settings import IMAGES_DIR, S3Settings, Storage, app_settings
from src.dal.file_storage.disk import DiskFileStorage
from src.dal.file_storage.s3 import S3FileStorage
from src.utils.logging.init_logger import init_logger


def _setup_s3_storage(app: FastAPI):
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


def _setup_disk_storage(app: FastAPI):
    app.state.file_storage = DiskFileStorage(images_dir=IMAGES_DIR)


def setup_storage(app: FastAPI):
    if app_settings.STORAGE == Storage.s3:
        _setup_s3_storage(app)
    elif app_settings.STORAGE == Storage.disk:
        _setup_disk_storage(app)
    else:
        raise ValueError('provided invalid storage type')


def setup_process_pool_executor(app: FastAPI):
    app.state.executor = ProcessPoolExecutor(max_workers=app_settings.IMAGE_PROCESSING_WORKERS)


def setup_middlewares(app: FastAPI):
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ErrorsMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def create_app() -> FastAPI:
    init_logger(
        name=app_settings.TITLE,
        is_debug=app_settings.IS_DEBUG
    )
    app = FastAPI(
        title=app_settings.TITLE,
        version=app_settings.VERSION,
    )
    setup_middlewares(app)
    setup_storage(app)
    setup_process_pool_executor(app)

    register_routers(
        app=app,
        routers=[*v1_routers]
    )

    return app
