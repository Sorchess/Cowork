from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.user import UserResponce


class CommentBase(BaseModel):
    content: str = Field(min_length=1, max_length=1024)


class CommentUpload(CommentBase):
    pass

class CommentDB(CommentBase):
    post_id: int
    author_id: int


class CommentOrder(Enum):
    POPULAR = "popular"
    NEW = "new"


class CommentPagination(BaseModel):
    limit: int = 20
    offset: int = 0
    order: CommentOrder = CommentOrder.POPULAR


class CommentResponse(BaseModel):
    comment_id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime
    author: UserResponce

    model_config = ConfigDict(from_attributes=True)
