from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from storages.banners.cache.cache_repo import BannerCacheRepository
from storages.banners.db.exceptions import (
    BannerNotFoundException,
    BannersConsistenceBrokenException,
)
from storages.banners.db.query_builders.get_by_feature_and_tag_id_builder import (
    GetUserBannerQueryBuilder,
)


class BannerRepository:
    def __init__(
        self, *, db_connection: AsyncSession, banner_cache: BannerCacheRepository
    ):
        self.db_connection = db_connection
        self.banner_cache = banner_cache

    async def get_by_feature_and_tag_id(
        self, *, user: "User", tag_id: int, feature_id: int
    ):
        query = GetUserBannerQueryBuilder.build(
            user=user, tag_id=tag_id, feature_id=feature_id
        )
        try:
            banner = (await self.db_connection.execute(query)).unique().scalar_one()
        except MultipleResultsFound as exc:
            raise BannersConsistenceBrokenException from exc
        except NoResultFound as exc:
            raise BannerNotFoundException from exc

        await self.banner_cache.save_banner_by_feature_and_tag_id(
            feature_id=feature_id, tag_id=tag_id, banner_content=banner.content
        )
        return banner.content
