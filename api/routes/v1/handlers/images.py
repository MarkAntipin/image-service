from fastapi import (APIRouter, Depends, File, HTTPException, Path, Response,
                     UploadFile, status)

from api.depends import get_images_service
from api.routes.v1.handlers.models import AddImage
from api.routes.v1.handlers.params import Size
from src.service.images import (ImageNotFoundError, ImagesService,
                                InvalidImageError)

router = APIRouter()


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=AddImage
)
async def add_image(
        file: UploadFile = File(...),
        images_service: ImagesService = Depends(get_images_service)
):
    try:
        image_id = await images_service.add_image(image=file)
    except InvalidImageError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail)
    return AddImage(image_id=image_id)


@router.get('/{width}x{height}/{image_id}')
async def get_image(
        image_id: str = Path(...),
        size: Size = Depends(),
        images_service: ImagesService = Depends(get_images_service)
):
    try:
        image = await images_service.get_image(image_id=image_id, width=size.width, height=size.height)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return Response(content=image.content, media_type=image.content_type)


@router.get('/{image_id}')
async def get_original_image(
        image_id: str = Path(...),
        images_service: ImagesService = Depends(get_images_service)
):
    try:
        image = await images_service.get_original_image(image_id=image_id)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return Response(content=image.content, media_type=image.content_type)
