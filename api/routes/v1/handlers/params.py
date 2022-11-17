from fastapi import HTTPException, Path, status

from settings import app_settings


class Size:
    def __init__(
            self,
            width: int = Path(..., gt=app_settings.IMAGE_MIN_WIDTH, lt=app_settings.IMAGE_MAX_WIDTH),
            height: int = Path(..., gt=app_settings.IMAGE_MIN_HEIGHT, lt=app_settings.IMAGE_MAX_HEIGHT),
    ):
        self._validate_size_step(width=width, height=height)
        self.width = width
        self.height = height

    @staticmethod
    def _validate_size_step(width: int, height: int):
        step = app_settings.SIZE_STEP
        if width % step + height % step != 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f'`width` and `height` must be a multiple of {app_settings.SIZE_STEP}'
            )
