from pydantic import BaseModel
from typing import Optional
from pydantic.config import ConfigDict


class CategoryBaseSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class CategoryCreateSchema(BaseModel):
    name: str

class CategoryUpdateSchema(BaseModel):
    name: str

class CategoryDeleteSchema(BaseModel):
    deleted_id: int
