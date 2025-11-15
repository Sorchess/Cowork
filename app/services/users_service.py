import logging

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from app.core.config import settings
from app.core.exceptions import (
    ObjectAlreadyExistsException,
    UserAlreadyExistsException,
    ObjectNotFoundException,
    UserNotFoundException,
    UserEmailNotVerificatedException,
    UnsupportedMediaTypeException,
    InvalidTokenException,
    DeprecatedTokenException,
)
from app.core.redis_manager import RedisStorage
from app.core.s3_client import S3Client
from app.models.user import DEFAULT_AVATAR_KEY
from app.repositories.users_repository import UsersRepository
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponce,
)
from app.schemas.token import TokenPayload, TokenScope
from app.schemas.confirmation import ConfirmationAction
from app.core import emails_publisher

from app.core.security import (
    hash_password,
    encode_jwt,
    decode_jwt,
    generate_uuid,
)
from app.services.emails_service import EmailsService

logger = logging.getLogger(__name__)

ALLOWED_CONTENT_TYPES = {"image/png", "image/jpeg", "image/webp"}


class UsersService:
    def __init__(
        self,
        repository: UsersRepository,
        s3_storage: S3Client,
        cache_storage: RedisStorage,
        emails_service: EmailsService,
    ):
        self.cache_storage = cache_storage
        self.s3_storage = s3_storage
        self.repository = repository
        self.emails_service = emails_service

    async def get_user_info(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> UserResponce:
        try:
            user = await self.repository.get_model(session=session, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        folder = "presets" if user.avatar == DEFAULT_AVATAR_KEY else "uploads"

        user.avatar_url = await self.s3_storage.get_presigned_url(
            folder=folder,
            file_name=user.avatar,
            expires_in=300,
        )

        return UserResponce.model_validate(user)

    async def create_user(
        self,
        user_create: UserCreate,
        session: AsyncSession,
    ) -> int:

        new_user = UserCreate(
            email=user_create.email,
            password=hash_password(user_create.password),
        )

        try:
            user = await self.repository.add(schema=new_user, session=session)
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException
        return user.id

    async def edit_user(
        self,
        user_id: int,
        session: AsyncSession,
        user_update: UserUpdate,
    ) -> None:
        try:
            user = await self.repository.get_one(session=session, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not user.email_verified:
            raise UserEmailNotVerificatedException

        await self.emails_service.send_confirmation_code(
            user=user,
            action=ConfirmationAction.EDIT_USER,
            payload=user_update.model_dump_json(),
        )

    async def change_avatar(
        self,
        session: AsyncSession,
        user_id: int,
        file: UploadFile,
    ) -> None:
        try:
            await self.repository.get_one(session=session, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if file.content_type not in ALLOWED_CONTENT_TYPES:
            raise UnsupportedMediaTypeException

        key = await self.s3_storage.upload_file(
            user_id=user_id,
            file=file,
        )

        await self.repository.patch(
            session=session, id=user_id, column="avatar", value=key
        )

    async def delete_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        try:
            user = await self.repository.get_one(session=session, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not user.email_verified:
            raise UserEmailNotVerificatedException

        await self.emails_service.send_confirmation_code(
            action=ConfirmationAction.USER_DELETION,
            user=user,
        )

    async def forgot_password(
        self,
        email: EmailStr,
        session: AsyncSession,
    ) -> None:
        try:
            user = await self.repository.get_one(session=session, email=email)
        except ObjectNotFoundException:
            raise UserNotFoundException

        if not user.email_verified:
            raise UserEmailNotVerificatedException

        payload = TokenPayload(
            user=user.id,
            jti=generate_uuid(),
            scope=TokenScope.PASSWORD_RESET,
        )
        token = encode_jwt(payload=payload)

        key = f"password_reset:user:{user.id}"
        expire = settings.jwt.ttl * 60

        await self.cache_storage.hset(
            key=key,
            values=payload.model_dump(),
            expire=expire,
        )

        await emails_publisher.publish(
            message={
                "email": user.email,
                "payload": token,
            },
        )

    async def reset_password(
        self,
        token: str,
        new_password: str,
        session: AsyncSession,
    ) -> None:
        payload = decode_jwt(token=token)

        if payload.get("scope") != TokenScope.PASSWORD_RESET:
            raise InvalidTokenException

        user_id = payload.get("sub")
        jti = payload.get("jti")

        if not user_id or not jti:
            raise InvalidTokenException

        key = f"password_reset:user:{user_id}"
        values = await self.cache_storage.hgetall(key=key)

        if not values:
            raise DeprecatedTokenException

        if values["jti"] != jti:
            raise InvalidTokenException
        try:
            user = await self.repository.get_one(session=session, id=int(user_id))
        except ObjectNotFoundException:
            raise UserNotFoundException

        user.password = hash_password(new_password)
        await self.repository.update(session=session, id=int(user_id), schema=user)
        await self.cache_storage.delete(key=key)

    async def verify_email(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        try:
            user = await self.repository.get_one(session=session, id=user_id)
        except ObjectNotFoundException:
            raise UserNotFoundException

        await self.emails_service.send_confirmation_code(
            action=ConfirmationAction.EMAIL_VERIFICATION,
            user=user,
        )
