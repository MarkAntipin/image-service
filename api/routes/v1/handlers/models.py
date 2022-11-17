from uuid import UUID

from pydantic import BaseModel


class AddImage(BaseModel):
    image_id: UUID
