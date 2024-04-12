from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from storages.models import BannerORM, BannerTagORM


class CheckBannerExistsQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def _select_banners(cls):
        cls.__result_query = select(BannerORM)
        return cls

    @classmethod
    def _join_tags(cls):
        cls.__result_query = cls.__result_query.join(BannerTagORM)
        return cls

    @classmethod
    def _filter_by_tag_ids(cls, *, tag_ids: list[int]):
        cls.__result_query = cls.__result_query.where(BannerTagORM.tag_id.in_(tag_ids))
        return cls

    @classmethod
    def _filter_by_feature_id(cls, *, feature_id: int):
        cls.__result_query = cls.__result_query.where(
            BannerORM.feature_id == feature_id
        )
        return cls

    @classmethod
    def _build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, feature_id: int, tag_ids: list[int]) -> Select:
        q = (
            cls._select_banners()
            ._join_tags()
            ._filter_by_tag_ids(tag_ids=tag_ids)
            ._filter_by_feature_id(feature_id=feature_id)
            ._build()
        )
        return q
