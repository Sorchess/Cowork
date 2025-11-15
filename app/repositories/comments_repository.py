from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Comment
from app.repositories.base_repository import BaseRepository
from app.schemas.comment import CommentPagination, CommentOrder, CommentResponse


class CommentsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Comment, CommentResponse)

    async def get_filtered(
        self, session: AsyncSession, pagination: CommentPagination, **kwargs
    ) -> list[CommentResponse]:
        stmt = (
            select(self.model)
            .filter_by(**kwargs)
            .options(selectinload(self.model.author))
        )
        if pagination.order == CommentOrder.POPULAR:

            stmt = stmt.order_by(
                asc(self.model.created_at),
                asc(self.model.comment_id),
            )
        else:
            stmt = stmt.order_by(
                desc(self.model.created_at),
                desc(self.model.comment_id),
            )

        result = await session.execute(stmt)
        result = result.scalars().all()
        return [self.schema.model_validate(instance) for instance in result]
