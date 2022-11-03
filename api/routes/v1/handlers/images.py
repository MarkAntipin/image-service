import io
from uuid import UUID

from fastapi import (APIRouter, Depends, File, HTTPException, Path, UploadFile,
                     status)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from src.service.images import (ImageNotFoundError, ImagesService,
                                InvalidImageError, get_images_service)

router = APIRouter()


class AddImage(BaseModel):
    image_id: UUID


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=AddImage
)
async def add_image(
        file: UploadFile = File(...),
        image_service: ImagesService = Depends(get_images_service)
):
    try:
        image_id = await image_service.add_image(image=file)
    except InvalidImageError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.detail
        )
    return AddImage(image_id=image_id)


@router.get('/{width}x{height}/{image_id}')
async def get_image(
        image_id: UUID = Path(...),
        # TODO: move max size to settings
        # TODO: create pagination for size (10, 20, 30...)
        width: int = Path(..., gt=1, lt=2000),
        height: int = Path(..., gt=1, lt=2000),
        image_service: ImagesService = Depends(get_images_service)
):
    try:
        image = await image_service.get_image(image_id=image_id, width=width, height=height)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return StreamingResponse(io.BytesIO(image))


@router.get('/{image_id}')
async def get_original_image(
        image_id: UUID = Path(...),
        image_service: ImagesService = Depends(get_images_service)
):
    try:
        image = await image_service.get_original_image(image_id=image_id)
    except ImageNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
    return StreamingResponse(io.BytesIO(image))
