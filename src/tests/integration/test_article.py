import pytest
from httpx import AsyncClient
from src.app.schemas.article import ArticleCreateSchema
from src.app.schemas.category import CategoryBaseSchema
from src.tests.utils.utils_article import (
    create_test_article,
    get_test_articles,
    update_test_article,
    soft_delete_test_article
)
from src.tests.fixtures.test_data import (
    test_categories_data, 
    test_articles_data, 
    test_article_update_data
)

@pytest.mark.asyncio
async def test_create_article(async_client):

    response = await create_test_article(
        async_client=async_client, 
        category_data=test_categories_data[0], 
        article_data=test_articles_data[0]
    )
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["title"] == test_articles_data[0]["title"]
    assert response_data["text"] == test_articles_data[0]["text"]
    assert response_data["category_id"] == test_articles_data[0]["category_id"]


@pytest.mark.asyncio
async def test_get_articles(async_client):

    get_response = await get_test_articles(
        async_client=async_client, 
        categories_data=test_categories_data, 
        articles_data=test_articles_data
    )
    
    assert get_response.status_code == 200
    assert len(get_response.json()) == 3
    
    # Тестируем поиск по названию
    search_response = await async_client.get("/articles/?search=Article 1")
    assert search_response.status_code == 200
    assert len(search_response.json()) == 1
    assert search_response.json()[0]["title"] == "Test Article 1"
    
    # # Тестируем фильтрацию по категории
    # category_response = await async_client.get(f"/articles/?category_id={cat1_id}")
    # assert category_response.status_code == 200
    # assert len(category_response.json()) == 1
    # assert category_response.json()[0]["category_id"] == cat1_id



@pytest.mark.asyncio
async def test_update_article(async_client):
    response = await update_test_article(
        async_client=async_client, 
        category_data=test_categories_data[0], 
        article_data=test_articles_data[0],
        article_update_data=test_article_update_data
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["title"] == test_article_update_data["title"]
    assert response_data["text"] == test_article_update_data["text"]

@pytest.mark.asyncio
async def test_soft_delete_article(async_client):
    # Создаем тестовую категорию
    delete_response = await soft_delete_test_article(
        async_client=async_client, 
        category_data=test_categories_data[0], 
        article_data=test_articles_data[0]
    )
    assert delete_response.status_code == 204
    
    # # Проверяем, что статья не видна в обычном списке
    # get_response = await async_client.get("/articles/")
    # assert len(get_response.json()) == 0
    
    # # Проверяем, что статья видна при show_deleted=True
    # get_deleted_response = await async_client.get("/articles/?show_deleted=true")
    # assert len(get_deleted_response.json()) == 1
    # assert get_deleted_response.json()[0]["id"] == article_id

