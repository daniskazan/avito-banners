import dataclasses

import jwt
from api.auth_exceptions import AdminOnlyAllowedException, AuthTokenRequiredException
from config.cache_client import caches
from fastapi import Depends
from fastapi.security import APIKeyHeader
from services.banner_service import BannerService
from storages.banners.cache.cache_repo import BannerCacheRepository
from storages.banners.db.db_repo import BannerRepository
from storages.banners.db.session import DatabaseConnection

api_key_header = APIKeyHeader(
    name="Authorization", description="Authorization token", auto_error=False
)


@dataclasses.dataclass
class User:
    sub: str
    admin: bool
    iat: int


async def get_user_or_401(api_token: str = Depends(api_key_header)) -> User:
    if not api_token:
        raise AuthTokenRequiredException
    try:
        payload = jwt.decode(api_token, "your-256-bit-secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError as exc:
        raise AuthTokenRequiredException from exc
    except jwt.InvalidSignatureError as exc:
        raise AuthTokenRequiredException from exc

    user = User(**payload)
    return user


async def admin_only(user: User = Depends(get_user_or_401)) -> User:
    if not user.admin:
        raise AdminOnlyAllowedException
    return user


async def get_db():
    yield DatabaseConnection
    await DatabaseConnection.close()


async def get_cache_client():
    return caches.get("default")


def get_banner_cache_repo(cache_client=Depends(get_cache_client)):
    return BannerCacheRepository(cache_client=cache_client)


def get_banner_repo(cache=Depends(get_banner_cache_repo), db=Depends(get_db)):
    return BannerRepository(db_connection=db, banner_cache=cache)


def get_banner_service(banner_repo: BannerRepository = Depends(get_banner_repo)):
    return BannerService(banner_repo=banner_repo)
