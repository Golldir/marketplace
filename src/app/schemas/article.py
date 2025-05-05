from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict


class ArticleBaseSchema(BaseModel):
    id: int
    title: str
    text: str
    category_id: int
    is_deleted: bool
    model_config = ConfigDict(from_attributes=True)

# TODO: нужен ли key в ответе? presigned_url нормальное название?
class ArticleGetSchema(BaseModel):
    id: int
    title: str
    text: str
    category_id: int
    presigned_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ArticleCreateSchema(BaseModel):
    title: str
    text: str
    category_id: int

class ArticleUpdateSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    category_id: Optional[int] = None

class ArticleDeleteSchema(BaseModel):
    id: int

