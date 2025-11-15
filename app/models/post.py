from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Integer,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.models.base import Base

if TYPE_CHECKING:  # Только для проверки типов
    from app.models.user import User
    from .comment import Comment
    from .file import File


class Post(Base):
    __tablename__ = "posts"

    post_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True,
    )
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.now,
    )
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    views: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
    comments_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # Relationships
    author: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
    )
    files: Mapped[list["File"]] = relationship(
        "File",
        back_populates="post",
        cascade="all, delete-orphan",
    )
