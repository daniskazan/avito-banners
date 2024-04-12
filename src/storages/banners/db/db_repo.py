from api.v1.banners.serializers.get_banner_list import GetBannersRequest
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from storages.banners.cache.cache_repo import BannerCacheRepository
from storages.banners.db.exceptions import (
    BannerNotFoundException,
    BannersConsistenceBrokenException,
)
from storages.banners.db.query_builders.get_banner_by_feature_and_tag_id import (
    GetUserBannerQueryBuilder,
)
from storages.banners.db.query_builders.get_banner_list_query import (
    GetUserBannerListQueryBuilder,
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

    async def get_banner_list(
        self, *, user: "User", params: GetBannersRequest
    ) -> list[RowMapping]:
        query = GetUserBannerListQueryBuilder.build(
            user=user,
            feature_id=params.feature_id,
            tag_id=params.tag_id,
            limit=params.limit,
            offset=params.offset,
        )
        result = await self.db_connection.execute(query)
        res: list[RowMapping] = [row._mapping for row in result.all()]  # noqa
        return res
