import jwt
from fastapi import Depends
from fastapi.security import APIKeyHeader
import dataclasses
from api.auth_exceptions import AuthTokenRequiredException, AdminOnlyAllowedException

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

    user = User(**payload)
    return user


async def admin_only(user: User = Depends(get_user_or_401)) -> User:
    if not user.admin:
        raise AdminOnlyAllowedException
    return user
