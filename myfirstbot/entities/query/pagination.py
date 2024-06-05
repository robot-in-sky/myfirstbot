from pydantic import BaseModel, PositiveInt


class Pagination(BaseModel):
    page: PositiveInt = 1
    per_page: PositiveInt = 10
