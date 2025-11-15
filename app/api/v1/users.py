from fastapi import APIRouter, Depends, status, File, UploadFile
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_user_id
from app.core import db_manager
from app.core.exceptions import (
    UserNotFoundException,
    UserNotFoundHTTPException,
    UserAlreadyExistsException,
    UserAlreadyExistsHTTPException,
    UserEmailNotVerificatedException,
    UserEmailNotVerificatedHTTPException,
)
from app.schemas.user import UserCreate, UserUpdate
from app.services import get_user_serivce
from app.services.users_service import UsersService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
async def get_personal_info(
    user_service: UsersService = Depends(get_user_serivce),
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        result = await user_service.get_user_info(
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "data": result,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.get("/{user_id:int}")
async def get_user(
    user_id: int,
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        result = await user_service.get_user_info(
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "data": result,
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post(
    "/sign-up",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user_create: UserCreate,
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        user_id = await user_service.create_user(
            user_create=user_create, session=session
        )
        return {
            "status": "success",
            "message": "User created successfully.",
            "id": user_id,
        }
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.patch("/edit")
async def edit_profile(
    user_update: UserUpdate,
    user_id: int = Depends(get_user_id),
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.edit_user(
            user_update=user_update,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserEmailNotVerificatedException:
        raise UserEmailNotVerificatedHTTPException


@router.delete("/delete")
async def delete_user(
    user_id: int = Depends(get_user_id),
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.delete_user(
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserEmailNotVerificatedException:
        raise UserEmailNotVerificatedHTTPException


@router.patch("/verify-email")
async def verify_email(
    user_service: UsersService = Depends(get_user_serivce),
    user_id: int = Depends(get_user_id),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.verify_email(
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Code sent successfully",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.patch("/change-avatar")
async def change_avatar(
    file: UploadFile = File(...),
    user_id: int = Depends(get_user_id),
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.change_avatar(
            file=file,
            user_id=user_id,
            session=session,
        )
        return {
            "status": "success",
            "message": "Avatar changed successfully.",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/forgot-password")
async def forgot_password(
    email: EmailStr,
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.forgot_password(
            email=email,
            session=session,
        )
        return {
            "status": "success",
            "message": "A link to restore access has been sent to your email.",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserEmailNotVerificatedException:
        raise UserEmailNotVerificatedHTTPException


@router.patch("/reset-password")  # TODO перенести ручку в подтверждения
async def reset_password(
    token: str,
    password: str,
    user_service: UsersService = Depends(get_user_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await user_service.reset_password(
            token=token,
            new_password=password,
            session=session,
        )
        return {
            "status": "success",
            "message": "Password reset successfully.",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
