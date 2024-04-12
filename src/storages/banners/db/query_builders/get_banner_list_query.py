from sqlalchemy import func, select
from sqlalchemy.sql.selectable import Select
from storages.models import BannerORM, BannerTagORM


class GetUserBannerListQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def _select_banners(cls):
        cls.__result_query = select(
            BannerORM.id,
            BannerORM.feature_id,
            BannerORM.content,
            BannerORM.created_at,
            BannerORM.is_active,
            func.array_agg(BannerTagORM.tag_id).label("tag_ids"),
        )
        return cls

    @classmethod
    def _join_tags(cls):
        cls.__result_query.join(BannerTagORM)
        return cls

    @classmethod
    def _filter_by_tag_id(cls, *, tag_id: int = None):
        if tag_id:
            cls.__result_query = cls.__result_query.where(BannerTagORM.tag_id == tag_id)
        return cls

    @classmethod
    def _filter_by_feature_id(cls, *, feature_id: int = None):
        if feature_id:
            cls.__result_query = cls.__result_query.where(
                BannerORM.feature_id == feature_id
            )
        return cls

    @classmethod
    def _filter_by_user_status(cls, *, user: "User"):
        if not user.admin:
            cls.__result_query = cls.__result_query.where(BannerORM.is_active.is_(True))
        return cls

    @classmethod
    def _group_by_banner_id(cls):
        cls.__result_query = cls.__result_query.group_by(BannerORM.id)
        return cls

    @classmethod
    def _apply_limit_offset(cls, *, limit: int, offset: int):
        cls.__result_query = cls.__result_query.limit(limit=limit).offset(offset=offset)
        return cls

    @classmethod
    def _build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(
        cls, *, user: "User", feature_id: int, tag_id: int, limit: int, offset: int
    ) -> Select:
        q = (
            cls._select_banners()
            ._join_tags()
            ._group_by_banner_id()
            ._filter_by_tag_id(tag_id=tag_id)
            ._filter_by_feature_id(feature_id=feature_id)
            ._filter_by_user_status(user=user)
            ._apply_limit_offset(limit=limit, offset=offset)
            ._build()
        )
        return q
