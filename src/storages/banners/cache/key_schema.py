class KeySchema:
    @classmethod
    def banner_hash_key(cls, feature_id: int, tag_id: int) -> str:
        return f"banners:{feature_id}:{tag_id}"
