import functools
import mimetypes
import typing as tp

import magic
from PIL import Image


def get_content_type(buffer: bytes) -> str:
    """ get content type of file by it's bytes with magic library
    """
    return magic.from_buffer(buffer=buffer, mime=True)


def get_extension(content_type: str) -> tp.Optional[str]:
    """ get file extension in dot prefix format ex: '.pdf' with mimetypes library
    """
    return mimetypes.guess_extension(type=content_type)


@functools.cache
def get_pil_format_from_content_type(content_type: str) -> tp.Optional[str]:
    """
    Get content type by PIL format
    PIL has specific format which differs from content type
    """
    for p_f, c_t in Image.MIME.items():
        if c_t == content_type:
            return p_f
    return None


def get_content_type_from_pil_format(pil_format: str) -> tp.Optional[str]:
    """
    Get PIL format by content type
    PIL has specific format which differs from content type
    """
    return Image.MIME.get(pil_format)
