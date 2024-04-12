from fastapi import FastAPI, status
from httpx import AsyncClient


async def test_get_banner_auth_client(app: FastAPI, auth_client: AsyncClient):
    response = await auth_client.get(
        url=app.url_path_for("banners:user_banner"),
        params={"feature_id": 111, "tag_id": 111, "use_last_revision": True},
    )
    assert response.status_code == 404

    response = await auth_client.get(
        url=app.url_path_for("banners:user_banner"),
        params={"feature_id": 111, "tag_id": 111, "use_last_revision": False},
    )
    assert response.status_code == 200


async def test_get_banner_no_auth(app: FastAPI, client: AsyncClient):
    response = await client.get(
        url=app.url_path_for("banners:user-banner"),
        params={"feature_id": 111, "tag_id": 111, "use_last_revision": True},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_create_banner_not_admin(app: FastAPI, auth_client: AsyncClient):
    response = await auth_client.post(
        url=app.url_path_for("banners:create-banner"),
        params={
            "feature_id": 111,
            "tag_ids": [111],
            "content": {"ok": False},
            "is_active": True,
        },
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN
