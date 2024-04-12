import uvicorn
from api.auth_exceptions import AuthTokenRequiredException
from api.router import router
from config.settings import settings
from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from storages.banners.db.session import async_engine
from storages.models import BaseORMModel
from utils.generic_response import APIResponse

app = FastAPI(title="Avito Tech Banner Service", default_response_class=APIResponse)
app.include_router(router=router)


@app.exception_handler(RequestValidationError)
def handler_422(request: Request, exc: RequestValidationError):  # noqa
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"error": exc.args}
    )


@app.exception_handler(AuthTokenRequiredException)
def handler_401(request: Request, exc: AuthTokenRequiredException):  # noqa
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "Пользователь не авторизован."},
    )


@app.exception_handler(Exception)
def handler_500(request: Request, exc: Exception):  # noqa
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"Внутренняя ошибка сервера. {exc.args}"},
    )


@app.on_event("startup")
async def init_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseORMModel.metadata.create_all)


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=settings.DEBUG,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        workers=settings.UVICORN_WORKERS,
    )
