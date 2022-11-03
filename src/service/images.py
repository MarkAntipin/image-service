import typing as tp
from uuid import UUID, uuid4

from fastapi import UploadFile

from settings import get_settings
from src.dal.file_storage.base import BaseFileStorage
from src.dal.file_storage.s3 import get_s3_file_storage
from src.utils.resize_image import resize_image


class InvalidImageError(Exception):

    def __init__(self, content_type):
        self.content_type = content_type
        self.detail = f'Image has unsupported content_type: {self.content_type}'


class ImageNotFoundError(Exception):

    def __init__(self):
        self.detail = 'Image not found'


class ImagesService:
    def __init__(self, file_storage: BaseFileStorage, allowed_image_types: tp.Set[str]):
        self._file_storage = file_storage
        self._allowed_image_types = allowed_image_types

    async def get_image(self, image_id: UUID, width: int, height: int) -> bytes:
        original_image = await self.get_original_image(image_id=image_id)
        resized_image = resize_image(image=original_image, width=width, height=height)
        return resized_image

    async def get_original_image(self, image_id: UUID) -> bytes:
        image_content = await self._file_storage.get(key=str(image_id))
        if not image_content:
            raise ImageNotFoundError()
        return image_content

    async def add_image(self, image: UploadFile) -> UUID:
        key = uuid4()
        self._validate_image(image=image)
        file = await image.read()
        await self._file_storage.set(key=str(key), file=file)
        return key

    def _validate_image(self, image: UploadFile) -> None:
        if image.content_type not in self._allowed_image_types:
            raise InvalidImageError(content_type=image.content_type)


def get_images_service() -> ImagesService:
    file_storage = get_s3_file_storage()
    settings = get_settings()

    return ImagesService(
        file_storage=file_storage,
        allowed_image_types=settings.ALLOWED_IMAGE_TYPES
    )
