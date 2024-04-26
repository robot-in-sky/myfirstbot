from typing import Any, TypeVar, overload

from pydantic import BaseModel, TypeAdapter

_PydanticModelT = TypeVar("_PydanticModelT", bound=BaseModel)


@overload
def to_pydantic(data: Any, return_type: type[_PydanticModelT]) -> _PydanticModelT:
    ...


@overload
def to_pydantic(data: Any, return_type: type[list[_PydanticModelT]]) -> list[_PydanticModelT]:
    ...


def to_pydantic(
        data: Any, return_type: type[_PydanticModelT] | type[list[_PydanticModelT]],
) -> _PydanticModelT | list[_PydanticModelT]:
    return_type_adapter: TypeAdapter[_PydanticModelT | list[_PydanticModelT]] = TypeAdapter(return_type)

    return return_type_adapter.validate_python(data)
