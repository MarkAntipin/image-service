import io
from uuid import UUID

from fastapi import (APIRouter, Depends, File, HTTPException, Path, UploadFile,
                     status)
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from settings import settings
from src.service.images import (ImageNotFoundError, ImagesService,
                                InvalidImageError, get_images_service)

router = APIRouter()


class AddImage(BaseModel):
    image_id: UUID


class Size:
    def __init__(
            self,
            width: int = Path(..., gt=settings.IMAGE_MIN_WIDTH, lt=settings.IMAGE_MAX_WIDTH),
            height: int = Path(..., gt=settings.IMAGE_MIN_HEIGHT, lt=settings.IMAGE_MAX_HEIGHT),
    ):
        self._validate_size_step(width=width, height=height)
        self.width = width
        self.height = height

    @staticmethod
    def _validate_size_step(width: int, height: int):
        step = settings.SIZE_STEP
        if width % step + height % step != 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'`width` and `height` must be a multiple of {settings.SIZE_STEP}'
            )


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
        size: Size = Depends(),
        image_service: ImagesService = Depends(get_images_service)
):
    try:
        image = await image_service.get_image(image_id=image_id, width=size.width, height=size.height)
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
