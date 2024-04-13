from dataclasses import dataclass

from api.v1.banners.serializers.create_banner import BannerCreateRequest
from api.v1.banners.serializers.get_banner_list import GetBannersRequest
from api.v1.banners.serializers.update_banner import BannerPartialUpdateRequest
from storages.banners.db.db_repo import BannerRepository


@dataclass
class BannerService:
    banner_repo: BannerRepository

    async def get_banner_by_feature_and_tag_id(
        self, *, user: "User", feature_id: int, tag_id: int, use_last_revision: bool
    ):
        if use_last_revision:
            return await self.banner_repo.get_by_feature_and_tag_id(
                user=user, tag_id=tag_id, feature_id=feature_id
            )
        return await self.banner_repo.banner_cache.get_banner_by_feature_and_tag_id(
            feature_id=feature_id, tag_id=tag_id
        )

    async def get_banner_list(self, *, user: "User", params: GetBannersRequest):
        return await self.banner_repo.get_banner_list(user=user, params=params)

    async def create_banner(self, *, params: BannerCreateRequest):
        return await self.banner_repo.create_banner(params=params)

    async def update_banner(
        self, *, banner_id: int, payload: BannerPartialUpdateRequest
    ):
        return await self.banner_repo.update_banner(
            banner_id=banner_id, payload=payload
        )

    async def delete_banner(self, *, banner_id: int):
        await self.banner_repo.delete_banner(banner_id=banner_id)

    async def delete_banners_by_feature_or_tag_id(
        self, *, feature_id: int | None, tag_id: int | None
    ):
        await self.banner_repo.delete_banners_by_feature_or_tag_id(
            feature_id=feature_id, tag_id=tag_id
        )

    async def get_banner_versions_list(self, *, banner_id: int):
        versions = await self.banner_repo.get_banner_versions_list(banner_id=banner_id)
        return versions
