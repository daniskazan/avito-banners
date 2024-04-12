import uvicorn

from config.settings import settings
from fastapi import (
    FastAPI,
    Request,
    status,
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.auth_exceptions import AuthTokenRequiredException

app = FastAPI(
    title="Avito Tech Banner Service",
)


@app.exception_handler(RequestValidationError)
def handler_422(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"error": str(exc)}
    )


@app.exception_handler(AuthTokenRequiredException)
def handler_401(request: Request, exc: AuthTokenRequiredException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "Пользователь не авторизован."},
    )


@app.exception_handler(Exception)
def handler_500(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"Внутренняя ошибка сервера. {exc.args}"},
    )


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        reload=settings.DEBUG,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        workers=settings.UVICORN_WORKERS,
    )
