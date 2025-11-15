from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .post import Post
    from .user import User


class Comment(Base):
    __tablename__ = "comments"

    comment_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True,
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.post_id", ondelete="CASCADE"), nullable=False
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )

    # Relationships
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments",
    )
    author: Mapped["User"] = relationship(
        "User",
        back_populates="comments",
    )
