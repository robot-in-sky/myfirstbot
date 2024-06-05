from typing import Literal

from pydantic import BaseModel

""" Sorting types """
ASC = "asc"
DESC = "desc"


class Sorting(BaseModel):
    order_by: str
    sort: Literal["asc", "desc"] = "asc"
