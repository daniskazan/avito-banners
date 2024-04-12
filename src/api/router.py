from api.v1.router import router as v1
from fastapi import APIRouter

router = APIRouter(prefix="/api")

router.include_router(v1)
