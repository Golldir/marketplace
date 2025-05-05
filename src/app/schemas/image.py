from pydantic import BaseModel

class ImageCreateSchema(BaseModel):
    article_id: int
    key: str
    hash: str
    type: str

class ImageGetSchema(BaseModel):
    id: int
    article_id: int
    key: str
    hash: str
    type: str

class ImageUpdateSchema(BaseModel):
    article_id: int
    key: str
    hash: str
    type: str

class ImageDeleteSchema(BaseModel):
    id: int
