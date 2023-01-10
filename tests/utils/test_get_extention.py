import pytest

from src.utils.image.utils import get_extension


@pytest.mark.parametrize(
    'content_type, extension', [
        ('image/jpeg', '.jpg'),
        ('image/png', '.png'),
        ('image/tiff', '.tiff'),
        ('application/pdf', '.pdf'),
    ])
def test_get_image_type(content_type, extension):
    res_extension = get_extension(content_type=content_type)
    assert res_extension == extension
