from dataclasses import dataclass

from api.v1.banners.serializers.get_banner_list import GetBannersRequest
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
