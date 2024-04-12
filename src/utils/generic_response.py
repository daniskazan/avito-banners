from typing import Generic, TypeVar

from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, alias_generators, conint


T = TypeVar("T")
ErrorDescription = TypeVar("ErrorDescription")


class APIResponse(JSONResponse, Generic[T]):
    """
    когда будем возвращать клиенту OkResponse/BadResponse
    этот класс проставит статус ответа в у самого объекта респонса
    """
    def render(self, content: T) -> bytes:
        if "statusCode" in content:
            self.status_code = content["statusCode"]
        return super().render(content=content)


class PydanticBaseModel(BaseModel):
    """
    Base model for all API Responses
    """

    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


class OkResponse(PydanticBaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status_code: conint(ge=200, le=299)
    payload: T

    @classmethod
    def new(cls, *, status_code: int, payload: T):
        return cls(status_code=status_code, payload=payload)


class BadResponse(PydanticBaseModel, Generic[ErrorDescription]):
    status_code: conint(ge=400, le=500)
    error: ErrorDescription

    @classmethod
    def new(cls, *, status_code: int, error: ErrorDescription):
        return cls(status_code=status_code, error=error)

