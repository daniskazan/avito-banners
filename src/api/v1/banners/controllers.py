from fastapi import APIRouter, Request, Depends

from src.api.v1.banners.dependencies import (
    get_user_or_401,
    User,
)

banners = APIRouter(prefix="/banners", tags=["Banners"])


@banners.get(
    "/user_banner",
    summary="Получение баннера для пользователя",
    name="banners:user_banner",
)
async def user_banner(
    request: Request,
    tag_id: int,
    feature_id: int,
    use_last_revision: bool = False,
    user: User = Depends(get_user_or_401),
):
    pass
