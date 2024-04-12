from api.v1.banners.serializers.create_banner import BannerCreateRequest
from api.v1.banners.serializers.get_banner_list import GetBannersRequest
from api.v1.banners.serializers.update_banner import BannerPartialUpdateRequest
from sqlalchemy import select
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from storages.banners.cache.cache_repo import BannerCacheRepository
from storages.banners.db.exceptions import (
    BannerNotFoundException,
    BannersConsistenceBrokenException,
    BannerWithSuchTagAndFeatureAlreadyExists,
    FeatureNotFoundException,
    TagNotFoundException,
)
from storages.banners.db.query_builders.check_banner_exists_query import (
    CheckBannerExistsQueryBuilder,
)
from storages.banners.db.query_builders.get_banner_by_feature_and_tag_id import (
    GetUserBannerQueryBuilder,
)
from storages.banners.db.query_builders.get_banner_list_query import (
    GetUserBannerListQueryBuilder,
)
from storages.models import BannerORM, FeatureORM, TagORM


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

    async def get_by_banner_id(self, *, banner_id: int) -> BannerORM:
        banner = await self.db_connection.get(BannerORM, {"id": banner_id})
        if not banner:
            raise BannerNotFoundException
        return banner

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

    async def create_banner(self, *, params: BannerCreateRequest):
        check_banner_exists_query = CheckBannerExistsQueryBuilder.build(
            feature_id=params.feature_id, tag_ids=params.tag_ids
        )
        banner_exists = (
            (await self.db_connection.execute(check_banner_exists_query))
            .unique()
            .scalars()
            .all()
        )
        if banner_exists:
            raise BannerWithSuchTagAndFeatureAlreadyExists

        tags_query = await self.db_connection.execute(
            select(TagORM).where(TagORM.id.in_(params.tag_ids))
        )
        tags_list = tags_query.unique().scalars().all()
        if len(tags_list) != len(params.tag_ids):
            raise TagNotFoundException

        feature = await self.db_connection.get(FeatureORM, {"id": params.feature_id})
        if not feature:
            raise FeatureNotFoundException

        banner = BannerORM(
            feature_id=feature.id,
            content=params.content,
            is_active=params.is_active,
        )
        banner.tags = tags_list
        self.db_connection.add(banner)
        await self.db_connection.commit()
        return banner.id

    async def update_banner(
        self, *, banner_id: int, payload: BannerPartialUpdateRequest
    ):
        banner_to_update: BannerORM = await self.get_by_banner_id(banner_id=banner_id)

        payload = payload.model_dump(exclude_none=True)
        feature_id, tag_ids = payload.get("feature_id"), payload.get("banner_tag_ids")
        if feature_id and tag_ids:
            check_banner_exists_query = CheckBannerExistsQueryBuilder.build(
                feature_id=feature_id, tag_ids=tag_ids
            )

            try:
                existing_banner = (
                    (await self.db_connection.execute(check_banner_exists_query))
                    .unique()
                    .scalar_one()
                )
            except NoResultFound:
                raise BannerNotFoundException from NoResultFound
            if existing_banner.id != banner_to_update.id:
                raise BannerWithSuchTagAndFeatureAlreadyExists

        if tag_ids:
            tags_to_add = (
                (
                    await self.db_connection.execute(
                        select(TagORM).where(TagORM.id.in_(tag_ids))
                    )
                )
                .unique()
                .scalars()
                .all()
            )
            if len(tags_to_add) != len(tag_ids):
                raise TagNotFoundException

            banner_to_update.tags.clear()
            for tag in tags_to_add:
                banner_to_update.tags.append(tag)

        # обновляем оставшиеся поля, помимо m2m
        for field, value in payload.items():
            setattr(banner_to_update, field, value)
        self.db_connection.add(banner_to_update)
        await self.db_connection.commit()
        return None
