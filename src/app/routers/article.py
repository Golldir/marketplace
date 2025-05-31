from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from src.app.dependencies.article import get_article_service
from typing import Annotated
from src.app.services.article import ArticleService
from src.app.schemas.article import (
    ArticleBaseSchema,
    ArticleCreateSchema,
    ArticleUpdateSchema,
    ArticleOutSchema
)
from fastapi import Form


router = APIRouter(prefix="/articles", tags=["Articles"])

def get_file_extension(filename: str) -> str:
    return filename.split('.')[-1]

@router.get("/", response_model=List[ArticleBaseSchema])
async def get_articles(
    article_service: Annotated[ArticleService, Depends(get_article_service)],
    search: Optional[str] = Query(None, description="Поиск по статьям"),
    category_id: Optional[int] = Query(None, description="Фильтрация по категории"),
    page_number: int = Query(1, ge=1, description="Номер страницы"),
    page_size: int = Query(10, ge=1, le=50, description="Размер страницы, максимум 50"),
    show_deleted: bool = Query(False, description="Показывать удаленные статьи")
):  
    return await article_service.get_articles(
        search=search,
        category_id=category_id,
        page_number=page_number,
        page_size=page_size,
        show_deleted=show_deleted
    )


@router.post("/", response_model=ArticleOutSchema, status_code=status.HTTP_201_CREATED)
async def create_article(
    article_service: Annotated[ArticleService, Depends(get_article_service)],
    title: str = Form(...),
    text: str = Form(...),
    category_id: int = Form(...)
):
    article_create_schema = ArticleCreateSchema(
        title=title,
        text=text,
        category_id=category_id
    )
    return await article_service.create_article(article_create_schema)


@router.put("/{article_id}", response_model=ArticleUpdateSchema, status_code=status.HTTP_200_OK)
async def update_article(
    article_service: Annotated[ArticleService, Depends(get_article_service)],
    article_id: int,
    title: Annotated[str | None, Form()] = None,
    text: Annotated[str | None, Form()] = None,
    category_id: Annotated[int | None, Form()] = None, 
):
    article_update_schema = ArticleUpdateSchema(
        id=article_id,
        title=title,
        text=text,
        category_id=category_id,
    )
    print('router', article_update_schema)
    return await article_service.update_article(article_id, article_update_schema)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def soft_delete_article(
    article_service: Annotated[ArticleService, Depends(get_article_service)],
    article_id: int
):
    res = await article_service.soft_delete_article(article_id)
    print('router', res)
    return res


