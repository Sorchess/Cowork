from fastapi import APIRouter

from .users import router as users_router
from .auth import router as auth_router
from .verifications import router as emails_router
from .posts import router as posts_router
from .files import router as storage_router

api_v1 = APIRouter(prefix="/v1")
api_v1.include_router(users_router)
api_v1.include_router(auth_router)
api_v1.include_router(emails_router)
api_v1.include_router(posts_router)
api_v1.include_router(storage_router)
