import io
import math

from PIL import Image


def resize_image(
        image: bytes,
        width: int,
        height: int,
        resample: int = Image.LANCZOS
) -> bytes:
    image = Image.open(io.BytesIO(image))

    image_format = image.format
    image = image.copy()

    im_w, im_h = image.size
    ratio = max(width / im_w, height / im_h)
    new_w = int(math.ceil(im_w * ratio))
    new_h = int(math.ceil(im_h * ratio))

    image = image.resize((new_w, new_h), resample)
    image = image.resize((new_w, new_h), Image.LANCZOS)
    im_w, im_h = image.size

    left = int(math.ceil((im_w - width) / 2))
    top = int(math.ceil((im_h - height) / 2))
    right = int(math.ceil(im_w - left))
    bottom = int(math.ceil(im_h - top))

    crop = image.crop((left, top, right, bottom))

    bytes_arr = io.BytesIO()
    crop.save(bytes_arr, format=image_format)
    return bytes_arr.getvalue()
