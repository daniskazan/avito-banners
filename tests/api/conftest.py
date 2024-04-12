import asyncio
from typing import Generator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(scope="session", autouse=True)
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def app() -> FastAPI:
    from main import app

    async with LifespanManager(app):
        yield app


@pytest.fixture()
async def user_token() -> str:
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOmZhbHNlLCJpYXQiOjE1MTYyMzkwMjJ9.BHogMyBoAFODgNGWUtiR9tl6wLO0Ib90g4dgZrOWhLE"
    return token


@pytest.fixture()
async def admin_token():
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.7DXwNbHtZoPUCoGv_Odt-jIOY2bBJDhBJeZKwpWCvCM"
    return token


@pytest.fixture()
async def client(app: FastAPI) -> AsyncClient:
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest.fixture()
async def auth_client(app: FastAPI, user_token: str):
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json", "Authorization": f"{user_token}"},
    ) as client:
        yield client


@pytest.fixture()
async def auth_admin_client(app: FastAPI, admin_token: str):
    async with AsyncClient(
        app=app,
        base_url="http://test",
        headers={"Content-Type": "application/json", "Authorization": f"{admin_token}"},
    ) as client:
        yield client
