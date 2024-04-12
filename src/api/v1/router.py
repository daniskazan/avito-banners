from api.v1.banners.controllers import banners
from fastapi import APIRouter

router = APIRouter(prefix="/v1")

router.include_router(banners)
