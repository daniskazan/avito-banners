import uuid

from pydantic import (
    Field,
)
from utils.generic_response import PydanticBaseModel


class GetBannerVersionHistoryResponse(PydanticBaseModel):
    banner_content: dict = Field(alias="content")
    version: uuid.UUID
    feature_id: int
    tag_ids: list[int]
