from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from storages.models import BannerORM, BannerTagORM


class GetUserBannerQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def _select_banners(cls):
        cls.__result_query = select(BannerORM)
        return cls

    @classmethod
    def _join_tags(cls):
        cls.__result_query = cls.__result_query.join(BannerORM.tags)
        return cls

    @classmethod
    def _filter_by_tag_id(cls, *, tag_id: int):
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
    def _build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, user: "User", feature_id: int, tag_id: int) -> Select:
        q = (
            cls._select_banners()
            ._join_tags()
            ._filter_by_tag_id(tag_id=tag_id)
            ._filter_by_feature_id(feature_id=feature_id)
            ._filter_by_user_status(user=user)
            ._build()
        )
        return q
