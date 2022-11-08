import typing as tp

import aioboto3
from botocore.exceptions import ClientError

from settings import settings
from src.dal.file_storage.base import BaseFileStorage


class S3FileStorage(BaseFileStorage):
    def __init__(self, bucket: str, session: aioboto3.Session) -> None:
        self._session = session
        self._bucket = bucket

    @property
    def client(self):
        return self._session.client('s3')

    async def set(self, key: str, file: bytes) -> None:
        async with self.client as c:
            await c.put_object(Body=file, Key=key, Bucket=self._bucket)

    async def get(self, key: str) -> tp.Optional[bytes]:
        async with self.client as c:
            try:
                r = await c.get_object(Bucket=self._bucket, Key=key)
            except ClientError:
                return None
            content = await r['Body'].read()
        return content


def get_s3_file_storage() -> S3FileStorage:
    session = aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.REGION_NAME
    )
    return S3FileStorage(session=session, bucket=settings.BUCKET)
