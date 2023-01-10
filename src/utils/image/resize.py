import io
import math
import typing as tp

from PIL import Image

from src.utils.image.utils import (get_content_type_from_pil_format,
                                   get_pil_format_from_content_type)


def _get_resample(ratio: float):
    if ratio > 1:
        resample = Image.BILINEAR
    else:
        resample = Image.NEAREST
    return resample


def resize_image(
        original_image: bytes,
        width: int,
        height: int,
        content_type: tp.Optional[str] = None,
) -> tp.Tuple[bytes, tp.Optional[str]]:
    pil_format = get_pil_format_from_content_type(content_type=content_type)
    image = Image.open(
        fp=io.BytesIO(original_image),
        formats=(pil_format,) if pil_format else None
    )
    pil_format = image.format

    im_w, im_h = image.size
    ratio = max(width / im_w, height / im_h)
    new_w = int(math.ceil(im_w * ratio))
    new_h = int(math.ceil(im_h * ratio))

    resample = _get_resample(ratio=ratio)
    image = image.resize((new_w, new_h), resample)

    im_w, im_h = image.size
    left = int(math.ceil((im_w - width) / 2))
    top = int(math.ceil((im_h - height) / 2))
    right = int(math.ceil(im_w - left))
    bottom = int(math.ceil(im_h - top))

    crop = image.crop((left, top, right, bottom))

    bytes_arr = io.BytesIO()
    crop.save(bytes_arr, format=pil_format)
    return (
        bytes_arr.getvalue(),
        get_content_type_from_pil_format(pil_format=pil_format) or content_type
    )
