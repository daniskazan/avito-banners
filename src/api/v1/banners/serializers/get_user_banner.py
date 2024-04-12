from pydantic import BaseModel


class GetUserBannerRequest(BaseModel):
    tag_id: int
    feature_id: int
    use_last_revision: bool = False
