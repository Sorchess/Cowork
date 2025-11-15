from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_user_id
from app.core import db_manager
from app.core.exceptions import (
    CommentNotFoundHTTPException,
    CommentNotFoundException,
    NotAuthorizedException,
    NotAuthorizedHTTPException,
    PostNotFoundHTTPException,
    PostNotFoundException,
    FileNotFoundException,
    FileNotFoundHTTPException,
)
from app.schemas.comment import CommentUpload, CommentPagination
from app.schemas.post import PostUpload
from app.services import get_posts_serivce, PostsService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/")
async def upload_post(
    post_upload: PostUpload,
    user_id: int = Depends(get_user_id),
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        data = await posts_service.upload_post(
            post_upload=post_upload,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Post uploaded successfully",
            "id": data,
        }
    except FileNotFoundException:
        raise FileNotFoundHTTPException
    except NotAuthorizedException:
        raise NotAuthorizedHTTPException


@router.get("/{post_id}")
async def get_post(
    post_id: int,
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        return await posts_service.get_post(
            post_id=post_id,
            session=session,
        )
    except PostNotFoundException:
        raise PostNotFoundHTTPException


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    user_id: int = Depends(get_user_id),
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await posts_service.delete_post(
            post_id=post_id,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Post deleted successfully.",
        }
    except PostNotFoundException:
        raise PostNotFoundHTTPException
    except NotAuthorizedException:
        raise NotAuthorizedHTTPException


@router.post("/{post_id}/comment")
async def comment(
    comment_upload: CommentUpload,
    post_id: int,
    user_id: int = Depends(get_user_id),
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        data = await posts_service.upload_comment(
            comment_upload=comment_upload,
            post_id=post_id,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Comment uploaded successfully.",
            "id": data,
        }
    except PostNotFoundException:
        raise PostNotFoundHTTPException


@router.get("/{post_id}/comments")
async def get_comments(
    post_id: int,
    pagination: CommentPagination = Depends(),
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        data = await posts_service.get_comments(
            post_id=post_id,
            pagination=pagination,
            session=session,
        )
        return {
            "status": "success",
            "data": data,
        }
    except PostNotFoundException:
        raise PostNotFoundHTTPException


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    user_id: int = Depends(get_user_id),
    posts_service: PostsService = Depends(get_posts_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await posts_service.delete_comment(
            comment_id=comment_id,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Comment deleted successfully.",
        }
    except CommentNotFoundException:
        raise CommentNotFoundHTTPException
    except NotAuthorizedException:
        raise NotAuthorizedHTTPException
