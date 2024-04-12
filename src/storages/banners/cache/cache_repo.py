from aiocache import BaseCache
from storages.banners.cache.key_schema import KeySchema


class BannerCacheRepository:
    def __init__(
        self, cache_client: BaseCache, key_schema: type[KeySchema] = KeySchema
    ):
        self.key_schema = key_schema
        self.cache_client = cache_client

    async def get_banner_by_feature_and_tag_id(self, feature_id: int, tag_id: int):
        banner_key = self.key_schema.banner_hash_key(
            feature_id=feature_id, tag_id=tag_id
        )
        return await self.cache_client.get(key=banner_key)

    async def save_banner_by_feature_and_tag_id(
        self, feature_id: int, tag_id: int, banner_content: dict, ttl: int = 5 * 60
    ):
        banner_key = self.key_schema.banner_hash_key(
            feature_id=feature_id, tag_id=tag_id
        )
        return await self.cache_client.set(
            key=banner_key, value=banner_content, ttl=ttl
        )
