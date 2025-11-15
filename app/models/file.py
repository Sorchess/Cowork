from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from .post import Post


class File(Base):
    __tablename__ = "files"

    file_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        unique=True,
        autoincrement=True,
        index=True,
    )
    key: Mapped[str] = mapped_column(String(255), nullable=False)
    origin: Mapped[str] = mapped_column(String(255))
    size: Mapped[int] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    post_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("posts.post_id", ondelete="CASCADE"),
        nullable=True,
    )

    # Relationships
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="files",
    )
