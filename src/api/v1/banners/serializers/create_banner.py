from pydantic import Field, PositiveInt
from utils.generic_response import PydanticBaseModel


class BannerCreateRequest(PydanticBaseModel):
    tag_ids: list[PositiveInt] = Field(description="ID тегов")
    feature_id: PositiveInt = Field(description="ID фичи")
    content: dict = Field(description="Контент баннера")
    is_active: bool = Field(description="Активность баннера", default=False)


class BannerCreateResponse(PydanticBaseModel):
    banner_id: PositiveInt = Field(description="ID нового баннера")
