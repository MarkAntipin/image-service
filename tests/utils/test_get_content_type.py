from src.utils.image.utils import get_content_type


def test_get_image_type(test_image_bytes):
    content_type = get_content_type(buffer=test_image_bytes[:2048])
    assert content_type == 'image/jpeg'


def test_get_pdf_type(test_pdf_bytes):
    content_type = get_content_type(buffer=test_pdf_bytes[:2048])
    assert content_type == 'application/pdf'
