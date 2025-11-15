from app.core import S3Client, cache_storage, sessions_storage, emails_publisher
from app.repositories.comments_repository import CommentsRepository
from app.repositories.files_repository import FilesRepository
from app.repositories.posts_repository import PostsRepository
from app.repositories.users_repository import UsersRepository
from app.services.auth_service import AuthService
from app.services.cookie_service import CookieService
from app.services.emails_service import EmailsService
from app.services.files_service import FilesService
from app.services.posts_service import PostsService
from app.services.users_service import UsersService


def get_emails_service() -> EmailsService:
    return EmailsService(
        publisher=emails_publisher,
        repository=UsersRepository(),
        auth_service=get_auth_serivce(),
        cache_storage=cache_storage,
    )


def get_user_serivce() -> UsersService:
    return UsersService(
        repository=UsersRepository(),
        s3_storage=S3Client(),
        emails_service=get_emails_service(),
        cache_storage=cache_storage,
    )


def get_auth_serivce() -> AuthService:
    return AuthService(
        repository=UsersRepository(),
        cookie_serivce=CookieService(),
        session_storage=sessions_storage,
    )


def get_files_serivce() -> FilesService:
    return FilesService(
        files_repository=FilesRepository(),
        s3_client=S3Client(),
    )


def get_posts_serivce() -> PostsService:
    return PostsService(
        posts_repository=PostsRepository(),
        files_repository=FilesRepository(),
        comments_repository=CommentsRepository(),
    )
