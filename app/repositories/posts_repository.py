from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ObjectNotFoundException
from app.models import Post
from app.repositories.base_repository import BaseRepository
from app.schemas.post import PostResponse


class PostsRepository(BaseRepository):
    def __init__(self):
        super().__init__(Post, PostResponse)

    async def get_post(self, session: AsyncSession, **kwargs):
        stmt = select(self.model).filter_by(**kwargs).options(selectinload(Post.files))
        result = await session.execute(stmt)
        try:
            post = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return post
