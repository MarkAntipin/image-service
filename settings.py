import typing as tp
from pathlib import Path

import dotenv
from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    PORT: int = 8080
    IS_DEBUG: bool = False

    TITLE: str = 'Image Service'
    VERSION: str = '0.1.0'

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    REGION_NAME: str
    BUCKET: str

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
        env_file = Path(BASE_DIR, '.env')
        dotenv.load_dotenv(env_file)


settings = Settings()
