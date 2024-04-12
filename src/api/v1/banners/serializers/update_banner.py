from pydantic import Field, PositiveInt
from utils.generic_response import PydanticBaseModel


class BannerPartialUpdateRequest(PydanticBaseModel):
    banner_tag_ids: list[PositiveInt] = Field(
        alias="tag_ids", default=None, description="ID тегов"
    )
    feature_id: PositiveInt = Field(default=None, description="ID фичи")
    content: dict = Field(default=None, description="Контент баннера")
    is_active: bool = Field(default=None, description="Активность баннера")
