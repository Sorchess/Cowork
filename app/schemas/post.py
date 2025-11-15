from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.models import File
from app.schemas.file import FileResponse


class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=8192)

class PostUpload(PostBase):
    files: list[str]


class PostDB(PostBase):
    author_id: int


class PostResponse(BaseModel):
    post_id: int
    title: str
    content: str
    created_at: datetime
    author_id: int
    views: int
    comments_count: int

    model_config = ConfigDict(from_attributes=True)
