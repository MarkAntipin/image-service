import abc
import typing as tp


# TODO: move to backend-utils
class SingletonABCMeta(abc.ABCMeta):
    """
    Singleton ABC metaclass
    """

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class BaseFileStorage(metaclass=SingletonABCMeta):

    @abc.abstractmethod
    async def set(self, key: str, file: bytes) -> None:
        ...

    @abc.abstractmethod
    async def get(self, key: str) -> tp.Optional[bytes]:
        ...
