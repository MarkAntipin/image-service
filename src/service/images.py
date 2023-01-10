import asyncio
import typing as tp
from concurrent.futures import ProcessPoolExecutor

from fastapi import UploadFile

from src.dal.file_storage.base import BaseFileStorage
from src.utils.image.resize import resize_image
from src.utils.image.types import ImageAdd, ImageGet


class InvalidImageError(Exception):

    def __init__(self, content_type):
        self.content_type = content_type
        self.detail = f'Image has unsupported content_type: {self.content_type}'


class ImageNotFoundError(Exception):

    def __init__(self):
        self.detail = 'Image not found'


class ImagesService:
    def __init__(
            self,
            file_storage: BaseFileStorage,
            allowed_image_types: tp.Set[str],
            executor: ProcessPoolExecutor
    ):
        self._file_storage = file_storage
        self._allowed_image_types = allowed_image_types
        self._executor = executor

    async def get_image(self, image_id: str, width: int, height: int) -> ImageGet:
        original_image: ImageGet = await self.get_original_image(image_id=image_id)
        #  TODO: https://www.youtube.com/watch?v=sFb7T3T1GO8
        loop = asyncio.get_running_loop()
        resized_image, content_type = await loop.run_in_executor(
            self._executor,
            resize_image,
            original_image.content,
            width,
            height,
            original_image.content_type
        )
        return ImageGet(content=resized_image, content_type=content_type)

    async def get_original_image(self, image_id: str) -> ImageGet:
        image: ImageGet = await self._file_storage.get(key=image_id)
        if not image:
            raise ImageNotFoundError()
        return image

    async def add_image(self, image: UploadFile) -> str:
        content = await image.read()
        # TODO: compress file
        # TODO: can use executor here
        image = ImageAdd.from_content(content=content)
        self._validate_image(content_type=image.content_type)
        await self._file_storage.add(file=image)
        return image.key

    def _validate_image(self, content_type: str) -> None:
        if content_type not in self._allowed_image_types:
            raise InvalidImageError(content_type=content_type)
