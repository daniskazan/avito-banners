# from sqlalchemy import delete
# from sqlalchemy.sql.dml import Delete
# from storages.models import BannerORM, BannerTagORM
#
#
# class DeleteBannersByFeatureOrTagQueryBuilder:
#     __result_query: Delete = ...
#
#     @classmethod
#     def _select_banners(cls):
#         cls.__result_query = delete(BannerORM)
#         return cls
#
#
#
#     @classmethod
#     def _filter_by_feature_id(cls, *, feature_id: int | None):
#         if feature_id:
#             cls.__result_query = cls.__result_query.filter(BannerORM.feature_id == feature_id)
#         return cls
#
#     @classmethod
#     def _filter_by_tag_id(cls, *, tag_id: int | None):
#         if tag_id:
#             cls.__result_query = cls.__result_query.filter(BannerORM.tags.any(id = tag_id))
#         return cls
#
#     @classmethod
#     def _build(cls) -> Delete:
#         return cls.__result_query
#
#     @classmethod
#     def build(cls, *, feature_id: int, tag_id: int) -> Delete:
#         q = (
#             cls._select_banners()
#             ._filter_by_tag_id(tag_id=tag_id)
#             ._filter_by_feature_id(feature_id=feature_id)
#             ._build()
#         )
#         return q


from sqlalchemy import delete
from sqlalchemy.sql.dml import Delete
from storages.models import BannerORM


class DeleteBannersByFeatureOrTagQueryBuilder:
    __result_query: Delete = ...

    @classmethod
    def _delete_banner(cls):
        cls.__result_query = delete(BannerORM)
        return cls

    @classmethod
    def _filter_by_feature_id(cls, *, feature_id: int | None):
        if feature_id:
            cls.__result_query = cls.__result_query.filter(
                BannerORM.feature_id == feature_id
            )
        return cls

    @classmethod
    def _filter_by_tag_id(cls, *, tag_id: int | None):
        if tag_id:
            cls.__result_query = cls.__result_query.filter(
                BannerORM.tags.any(id=tag_id)
            )
        return cls

    @classmethod
    def _build(cls) -> Delete:
        return cls.__result_query

    @classmethod
    def build(cls, *, feature_id: int, tag_id: int) -> Delete:
        q = (
            cls._delete_banner()
            ._filter_by_tag_id(tag_id=tag_id)
            ._filter_by_feature_id(feature_id=feature_id)
            ._build()
        )
        return q
