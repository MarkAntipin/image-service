import typing as tp
import uuid

from pydantic import BaseModel

from src.utils.image.utils import get_content_type, get_extension


class Image(BaseModel):
    content: bytes
    content_type: tp.Optional[str]


class ImageAdd(Image):
    """ Image to set into storage
    """
    key: str

    @classmethod
    def from_content(cls, content: bytes):
        content_type = get_content_type(buffer=content[:2048])
        extension = get_extension(content_type=content_type)
        key = str(uuid.uuid4())
        if extension:
            key = f'{key}{extension}'

        return cls(
            content=content,
            content_type=content_type,
            key=key
        )


class ImageGet(Image):
    """ Image to get from storage
    """
