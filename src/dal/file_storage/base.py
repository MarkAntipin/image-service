import abc
import typing as tp

from src.utils.image.types import ImageAdd, ImageGet


class BaseFileStorage:

    @abc.abstractmethod
    async def add(self, file: ImageAdd) -> None:
        ...

    @abc.abstractmethod
    async def get(self, key: str) -> tp.Optional[ImageGet]:
        ...
