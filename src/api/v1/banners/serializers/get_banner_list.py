import datetime as dt

from fastapi import Query
from fastapi.exceptions import RequestValidationError
from pydantic import (
    Field,
    PositiveInt,
    StrictInt,
    ValidationInfo,
    field_validator,
)
from utils.generic_response import PydanticBaseModel


class GetBannersRequest(PydanticBaseModel):
    feature_id: PositiveInt | None = Field(default=Query(default=None))
    tag_id: PositiveInt | None = Field(default=Query(default=None))

    limit: PositiveInt = Field(default=Query(default=100))
    offset: StrictInt = Field(default=Query(default=0))

    @field_validator("tag_id")
    @classmethod
    def tag_id_or_feature_id_required(cls, tag_id: int | None, values: ValidationInfo):
        if not values.data.get("feature_id") and not tag_id:
            raise RequestValidationError("tagId or featureId required")
        return tag_id


class GetBannersResponse(PydanticBaseModel):
    id: int = Field(alias="banner_id")
    tag_ids: list[int] = Field(alias="tag_ids")
    feature_id: int
    content: dict
    is_active: bool
    created_at: dt.datetime
