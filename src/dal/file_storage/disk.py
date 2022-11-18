import typing as tp
from pathlib import Path

import aiofiles

from src.dal.file_storage.base import BaseFileStorage


# TODO: only for testing purposes; Upgrade for production usage
class DiskFileStorage(BaseFileStorage):
    def __init__(self, images_dir: Path):
        self.images_dir = images_dir
        self.images_dir.mkdir(exist_ok=True)

    async def set(self, key: str, file: bytes) -> None:
        async with aiofiles.open(Path(self.images_dir, key), 'wb') as f:
            await f.write(file)

    async def get(self, key: str) -> tp.Optional[bytes]:
        image_path = Path(self.images_dir, key)
        if not image_path.exists():
            return None

        async with aiofiles.open(Path(self.images_dir, key), 'rb') as f:
            content = await f.read()
        return content
