import typing as tp
from enum import auto
from pathlib import Path

import dotenv
from backend_utils.tools import StrEnum
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent
IMAGES_DIR = Path(BASE_DIR, 'images')

ENV_FILE = Path(BASE_DIR, '.env')
dotenv.load_dotenv(ENV_FILE)


class Storage(StrEnum):
    s3 = auto()
    disk = auto()


class S3Settings(BaseSettings):
    ACCESS_KEY_ID: str
    SECRET_ACCESS_KEY: str
    BUCKET: str
    REGION_NAME: tp.Optional[str] = None
    ENDPOINT_URL: tp.Optional[str] = None

    class Config:
        case_sensitive = False
        env_prefix = "S3_"


class AppSettings(BaseSettings):
    PORT: int = 8080
    IS_DEBUG: bool = False

    TITLE: str = 'Image Service'
    VERSION: str = '0.1.0'

    STORAGE: Storage = Storage.s3

    IMAGE_MIN_WIDTH: int = 10
    IMAGE_MIN_HEIGHT: int = 10
    IMAGE_MAX_WIDTH: int = 2000
    IMAGE_MAX_HEIGHT: int = 2000
    SIZE_STEP: int = 10

    ALLOWED_IMAGE_TYPES: tp.Set[str] = {
        'image/jpeg',
        'image/jpg',
        'image/png',
        'image/tiff'
    }

    class Config:
        case_sensitive = False


app_settings = AppSettings()
