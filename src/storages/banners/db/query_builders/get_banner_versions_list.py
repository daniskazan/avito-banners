from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from storages.models import BannerVersionHistory


class GetBannerVersionListQueryBuilder:
    __result_query: Select = ...

    @classmethod
    def _select_banners(cls):
        cls.__result_query = select(BannerVersionHistory)
        return cls

    @classmethod
    def _filter_by_banner_id(cls, *, banner_id: int):
        cls.__result_query = cls.__result_query.where(
            BannerVersionHistory.banner_id == banner_id
        )
        return cls

    @classmethod
    def _order_by_created_at_desc(cls):
        cls.__result_query = cls.__result_query.order_by(
            BannerVersionHistory.created_at.desc()
        )
        return cls

    @classmethod
    def _build(cls) -> Select:
        return cls.__result_query

    @classmethod
    def build(cls, *, banner_id: int) -> Select:
        q = (
            cls._select_banners()
            ._filter_by_banner_id(banner_id=banner_id)
            ._order_by_created_at_desc()
            ._build()
        )
        return q
