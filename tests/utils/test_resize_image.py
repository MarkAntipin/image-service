import io

import pytest
from PIL import Image

from src.utils.resize_image import resize_image


@pytest.mark.parametrize(
    'width,height', [
        (100, 2000),
        (1000, 1000),
    ])
def test_resize_image(mock_env, test_image_bytes, width, height):
    resized_image = resize_image(
        image=test_image_bytes,
        width=width,
        height=height
    )
    resized_image = Image.open(io.BytesIO(resized_image))
    image_w, image_h = resized_image.size
    assert image_w == width
    assert image_h == height
