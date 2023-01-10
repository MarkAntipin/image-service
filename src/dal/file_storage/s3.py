import typing as tp

import aioboto3
from botocore.exceptions import ClientError

from src.dal.file_storage.base import BaseFileStorage
from src.utils.image.types import ImageAdd, ImageGet


class S3FileStorage(BaseFileStorage):
    def __init__(
            self,
            bucket: str,
            session: aioboto3.Session,
            endpoint_url: tp.Optional[str] = None
    ) -> None:
        self._session = session
        self._bucket = bucket
        self._endpoint_url = endpoint_url

    @property
    def client(self):
        return self._session.client('s3', endpoint_url=self._endpoint_url)

    async def add(self, file: ImageAdd) -> None:
        metadata = {}
        if file.content_type:
            metadata['content-type'] = file.content_type

        async with self.client as c:
            await c.put_object(
                Body=file.content,
                Key=file.key,
                Bucket=self._bucket,
                Metadata=metadata
            )

    async def get(self, key: str) -> tp.Optional[ImageGet]:
        async with self.client as c:
            try:
                r = await c.get_object(Bucket=self._bucket, Key=key)
            except ClientError:
                return None
            content = await r['Body'].read()
            content_type = r['Metadata'].get('content-type')
        return ImageGet(content=content, content_type=content_type)
