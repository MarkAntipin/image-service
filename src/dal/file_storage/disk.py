import typing as tp
from pathlib import Path

import aiofiles

from src.dal.file_storage.base import BaseFileStorage
from src.utils.image.types import ImageAdd, ImageGet


# TODO: only for testing purposes; Upgrade for production usage
class DiskFileStorage(BaseFileStorage):
    def __init__(self, images_dir: Path):
        self.images_dir = images_dir
        self.images_dir.mkdir(exist_ok=True)

    async def add(self, file: ImageAdd) -> None:
        file_path = Path(self.images_dir, file.key)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file.content)

    async def get(self, key: str) -> tp.Optional[ImageGet]:
        image_path = Path(self.images_dir, key)
        if not image_path.exists():
            return None

        async with aiofiles.open(Path(self.images_dir, key), 'rb') as f:
            content = await f.read()
        return content
