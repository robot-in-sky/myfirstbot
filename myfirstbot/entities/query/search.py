from pydantic import BaseModel


class Search(BaseModel):
    s: str
    fields: set[str]
