from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    PostNotFoundException,
    ObjectNotFoundException,
    FileNotFoundException,
    NotAuthorizedException,
    CommentNotFoundException,
)
from app.models import Post
from app.repositories.comments_repository import CommentsRepository
from app.repositories.files_repository import FilesRepository
from app.repositories.posts_repository import PostsRepository
from app.schemas.comment import (
    CommentUpload,
    CommentPagination,
    CommentDB,
    CommentResponse,
)
from app.schemas.post import PostUpload, PostDB


class PostsService:
    def __init__(
        self,
        posts_repository: PostsRepository,
        files_repository: FilesRepository,
        comments_repository: CommentsRepository,
    ):
        self.posts = posts_repository
        self.files = files_repository
        self.comments = comments_repository

    async def get_post(
        self,
        post_id: int,
        session: AsyncSession,
    ) -> Post:
        try:
            return await self.posts.get_post(session=session, post_id=post_id)
        except ObjectNotFoundException:
            raise PostNotFoundException

    async def upload_post(
        self,
        post_upload: PostUpload,
        user_id: int,
        session: AsyncSession,
    ) -> int:
        post = PostDB(
            title=post_upload.title,
            content=post_upload.content,
            author_id=user_id,
        )

        result = await self.posts.add(session=session, schema=post)

        if post_upload.files:
            for key in post_upload.files:
                try:
                    file = await self.files.get_one(session=session, key=key)
                except ObjectNotFoundException:
                    raise FileNotFoundException

                if file.author_id != user_id:
                    raise NotAuthorizedException

                await self.files.patch(
                    session=session, column="post_id", value=result.post_id, key=key
                )
        return result.post_id

    async def delete_post(
        self,
        post_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        try:
            post = await self.posts.get_one(session=session, post_id=post_id)
        except ObjectNotFoundException:
            raise PostNotFoundException

        if post.author_id != user_id:
            raise NotAuthorizedException

        await self.posts.delete(session=session, post_id=post_id)

    async def upload_comment(
        self,
        comment_upload: CommentUpload,
        post_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> int:
        try:
            post = await self.posts.get_one(session=session, post_id=post_id)
        except ObjectNotFoundException:
            raise PostNotFoundException

        comment = CommentDB(
            post_id=post_id,
            content=comment_upload.content,
            author_id=user_id,
        )

        comment = await self.comments.add(session=session, schema=comment)
        await self.posts.patch(
            session=session,
            column="comments_count",
            value=post.comments_count + 1,
            post_id=post_id,
        )
        return comment.comment_id

    async def get_comments(
        self,
        post_id: int,
        pagination: CommentPagination,
        session: AsyncSession,
    ) -> list[CommentResponse]:
        try:
            await self.posts.get_one(session=session, post_id=post_id)
        except ObjectNotFoundException:
            raise PostNotFoundException

        return await self.comments.get_filtered(
            session=session, pagination=pagination, post_id=post_id
        )

    async def delete_comment(
        self,
        comment_id: int,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        try:
            comment = await self.comments.get_model(
                session=session,
                comment_id=comment_id,
            )
        except ObjectNotFoundException:
            raise CommentNotFoundException

        if comment.author_id != user_id:
            raise NotAuthorizedException

        await self.comments.delete(session=session, comment_id=comment_id)
        await self.posts.patch(
            session=session,
            column="comments_count",
            value=func.greatest(Post.comments_count - 1, 0),
            post_id=comment.post_id,
        )
