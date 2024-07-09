from collections.abc import Sequence
from enum import Enum
from math import ceil
from typing import Any, Generic, TypeVar

from fastapi_pagination import Page, Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import BaseModel, Field

DataType = TypeVar("DataType")
T = TypeVar("T")


class IOrderEnum(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"


# basic schemas
class UserIdentity(BaseModel):
    id: str
    email: str


class ApiKeyIdentity(BaseModel):
    api_key: str


class SupabaseAccessToken(BaseModel):
    sub: str
    email: str


# API response schemas


class PageBase(Page[T], Generic[T]):
    previous_page: int | None = Field(
        default=None, description="Page number of the previous page"
    )
    next_page: int | None = Field(
        default=None, description="Page number of the next page"
    )


class IResponseBase(BaseModel, Generic[T]):
    message: str = ""
    meta: dict | Any | None = {}
    data: T | None = None


class IGetResponsePaginated(AbstractPage[T], Generic[T]):
    message: str | None = ""
    meta: dict = {}
    data: PageBase[T]

    __params_type__ = Params  # Set params related to Page

    @classmethod
    def create(
        cls,
        items: Sequence[T],
        total: int,
        params: AbstractParams,
    ) -> PageBase[T] | None:
        if params.size is not None and total is not None and params.size != 0:
            pages = ceil(total / params.size)
        else:
            pages = 0

        return cls(
            data=PageBase[T](
                items=items,
                page=params.page,
                size=params.size,
                total=total,
                pages=pages,
                next_page=params.page + 1 if params.page < pages else None,
                previous_page=params.page - 1 if params.page > 1 else None,
            )
        )


class IGetResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data got correctly"


class IPostResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data created correctly"


class IPutResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data updated correctly"


class IDeleteResponseBase(IResponseBase[DataType], Generic[DataType]):
    message: str | None = "Data deleted correctly"


def create_response(
    data: DataType,
    message: str | None = None,
    meta: dict | Any | None = {},
) -> (
    IResponseBase[DataType]
    | IGetResponsePaginated[DataType]
    | IGetResponseBase[DataType]
    | IPutResponseBase[DataType]
    | IDeleteResponseBase[DataType]
    | IPostResponseBase[DataType]
):
    if isinstance(data, IGetResponsePaginated):
        data.message = "Data paginated correctly" if message is None else message
        data.meta = meta
        return data
    if message is None:
        return {"data": data, "meta": meta}
    return {"data": data, "message": message, "meta": meta}
