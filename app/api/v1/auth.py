from fastapi import APIRouter, Response, Depends, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_manager
from app.core.exceptions import (
    UserNotFoundException,
    UserWrongPasswordException,
    UserNotFoundHTTPException,
    UserWrongPasswordHTTPException,
    InvalidSessionCookieHTTPException,
    InvalidSessionCookieException,
)
from app.schemas.user import UserCredentials
from app.services import AuthService, get_auth_serivce

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/sign-in")
async def sign_in(
    response: Response,
    user_credentials: UserCredentials,
    auth_service: AuthService = Depends(get_auth_serivce),
    session: AsyncSession = Depends(db_manager.session_getter),
):
    try:
        await auth_service.sign_in(
            response=response,
            user_credentials=user_credentials,
            session=session,
        )
        return {
            "status": "success",
            "message": "You have successfully logged in.",
        }
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except UserWrongPasswordException:
        raise UserWrongPasswordHTTPException


@router.post("/logout")
async def logout(
    response: Response,
    request: Request,
    auth_service: AuthService = Depends(get_auth_serivce),
):
    try:
        await auth_service.logout(
            response=response,
            request=request,
        )
        return {
            "status": "success",
            "message": "You have successfully logged out.",
        }
    except InvalidSessionCookieException:
        raise InvalidSessionCookieHTTPException
