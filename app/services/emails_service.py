import json

from faststream.rabbit.publisher import RabbitPublisher
from pydantic import SecretStr
from fastapi import Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import InvalidTokenException, TooManyAttemptsException
from app.core.redis_manager import RedisStorage
from app.repositories.users_repository import UsersRepository
from app.schemas.confirmation import ConfirmationRequest, ConfirmationAction
from app.schemas.user import UserResponce, UserUpdate
from app.core.security import hash_password, verify_password, generate_secret_code
from app.services import AuthService


class EmailsService:
    def __init__(
        self,
        repository: UsersRepository,
        publisher: RabbitPublisher,
        cache_storage: RedisStorage,
        auth_service: AuthService,
    ):
        self.repository = repository
        self.publisher = publisher
        self.cache_storage = cache_storage
        self.auth_service = auth_service

    @staticmethod
    def _redis_keys(user_id: int) -> str:
        return f"confirm:user:{user_id}"

    async def send_confirmation_code(
        self,
        action: ConfirmationAction,
        user: UserResponce,
        payload: str = "",
    ) -> None:
        key = self._redis_keys(user_id=user.id)

        code = generate_secret_code()
        code_hash = hash_password(code)

        values = ConfirmationRequest(action=action, code=code_hash, payload=payload)
        expire = settings.verification.ttl * 60

        await self.cache_storage.hset(
            key=key,
            values=values.model_dump(),
            expire=expire,
        )

        await self.publisher.publish(
            message={
                "email": user.email,
                "payload": code,
            },
        )

    async def verify_code(
        self,
        user_id: int,
        code: SecretStr,
        session: AsyncSession,
        response: Response,
        request: Request,
    ) -> None:

        key = self._redis_keys(user_id=user_id)
        values = await self.cache_storage.hgetall(key=key)

        if not values:
            raise InvalidTokenException

        if not verify_password(
            password=code.get_secret_value(),
            hashed_password=values["code"],
        ):
            values["attempts"] -= 1

            await self.cache_storage.hset(
                key=key,
                values=values.model_dump(),
            )

            if int(values["attempts"] or 0) <= 0:
                await self.cache_storage.delete(
                    key=key,
                )
                raise TooManyAttemptsException

            raise InvalidTokenException

        await self.cache_storage.delete(key=key)

        action = values["action"]

        if action == ConfirmationAction.EMAIL_VERIFICATION:
            await self._email_verification(
                user_id=user_id,
                session=session,
            )

        elif action == ConfirmationAction.USER_DELETION:
            await self._user_deletion(
                user_id=user_id,
                session=session,
                response=response,
                request=request,
            )
        elif action == ConfirmationAction.EDIT_USER:
            await self._edit_user(
                user_id=user_id,
                session=session,
                data=values["payload"],
            )
        else:
            raise InvalidTokenException

    async def _email_verification(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> None:
        # TODO исправить верификацию, перенести эти методы в users_service, а здесь сделать отправку письма
        await self.repository.patch(
            session=session, id=user_id, column="email_verified", value=True
        )

    async def _edit_user(
        self,
        user_id: int,
        session: AsyncSession,
        data: str,
    ) -> None:
        user = UserUpdate()
        # меняем данные
        for key, value in json.loads(data).items():
            if key == "password":
                setattr(user, "password", hash_password(value))
            else:
                if key == "email":
                    user.email_verified = False

                setattr(user, key, value)

        await self.repository.update(session=session, id=user_id, schema=user)

    async def _user_deletion(
        self,
        user_id: int,
        session: AsyncSession,
        response: Response,
        request: Request,
    ) -> None:
        await self.repository.delete(session=session, id=user_id)

        await self.auth_service.logout(
            response=response,
            request=request,
        )
