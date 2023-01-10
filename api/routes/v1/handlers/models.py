from pydantic import BaseModel


class AddImage(BaseModel):
    image_id: str
