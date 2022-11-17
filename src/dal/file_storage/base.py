import abc
import typing as tp


class BaseFileStorage:

    @abc.abstractmethod
    async def set(self, key: str, file: bytes) -> None:
        ...

    @abc.abstractmethod
    async def get(self, key: str) -> tp.Optional[bytes]:
        ...
