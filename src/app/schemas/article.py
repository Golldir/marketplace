from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict
from src.app.schemas.image import ImageWithURLSchema
from typing import List

class ArticleBaseSchema(BaseModel):
    id: int
    title: str
    text: str
    category_id: int
    is_deleted: bool = False
    images: Optional[List[ImageWithURLSchema]] = None
    model_config = ConfigDict(from_attributes=True)

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

class ArticleOutSchema(BaseModel):
    id: int
    title: str
    text: str
    category_id: int

class ArticleUpdateSchema(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    category_id: Optional[int] = None

class ArticleDeleteSchema(BaseModel):
    id: int

