from concurrent.futures import ProcessPoolExecutor

from fastapi import Request

from settings import app_settings
from src.dal.file_storage.base import BaseFileStorage
from src.service.images import ImagesService


def get_file_storage(request: Request) -> BaseFileStorage:
    return request.app.state.file_storage


def get_executor(request: Request) -> ProcessPoolExecutor:
    return request.app.state.executor


def get_images_service(request: Request) -> ImagesService:
    file_storage = get_file_storage(request)
    return ImagesService(
        file_storage=file_storage,
        allowed_image_types=app_settings.ALLOWED_IMAGE_TYPES,
        executor=get_executor(request)
    )
