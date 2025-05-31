import pytest
from fastapi import UploadFile
from pathlib import Path
from src.tests.utils.utils_image import create_test_image

@pytest.mark.asyncio
async def test_create_image(async_client):
    # Создаем тестовое изображение

    response = await create_test_image(async_client)
    
    print('response', response.json())
    assert response.status_code == 200







    
#     # Создаем тестовую статью
#     article_data = {
#         "title": "Test Article",
#         "text": "Test Text",
#         "category_id": cat_id
#     }
#     article_response = await async_client.post(
#         "/articles/",
#         data=article_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     article_id = article_response.json()["id"]
    
#     # Создаем изображение
#     image_data = {
#         "article_id": article_id,
#         "key": "test_image.jpg",
#         "hash": "abc123",
#         "type": "image/jpeg"
#     }
    
#     response = await async_client.post("/images/", json=image_data)
#     assert response.status_code == 201
#     assert response.json()["article_id"] == image_data["article_id"]
#     assert response.json()["key"] == image_data["key"]
#     assert response.json()["hash"] == image_data["hash"]
#     assert response.json()["type"] == image_data["type"]

# @pytest.mark.asyncio
# async def test_get_images(async_client):
#     # Создаем тестовую категорию
#     category = {"name": "Test Category"}
#     cat_response = await async_client.post("/categories/", json=category)
#     cat_id = cat_response.json()['id']
    
#     # Создаем тестовую статью
#     article_data = {
#         "title": "Test Article",
#         "text": "Test Text",
#         "category_id": cat_id
#     }
#     article_response = await async_client.post(
#         "/articles/",
#         data=article_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     article_id = article_response.json()["id"]
    
#     # Создаем несколько изображений
#     image1 = {
#         "article_id": article_id,
#         "key": "test_image1.jpg",
#         "hash": "abc123",
#         "type": "image/jpeg"
#     }
#     image2 = {
#         "article_id": article_id,
#         "key": "test_image2.jpg",
#         "hash": "def456",
#         "type": "image/jpeg"
#     }
    
#     await async_client.post("/images/", json=image1)
#     await async_client.post("/images/", json=image2)
    
#     # Получаем все изображения
#     response = await async_client.get(f"/images/article/{article_id}")
#     assert response.status_code == 200
#     assert len(response.json()) == 2

# @pytest.mark.asyncio
# async def test_update_image(async_client):
#     # Создаем тестовую категорию и статью
#     category = {"name": "Test Category"}
#     cat_response = await async_client.post("/categories/", json=category)
#     cat_id = cat_response.json()['id']
    
#     article_data = {
#         "title": "Test Article",
#         "text": "Test Text",
#         "category_id": cat_id
#     }
#     article_response = await async_client.post(
#         "/articles/",
#         data=article_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     article_id = article_response.json()["id"]
    
#     # Создаем изображение
#     image_data = {
#         "article_id": article_id,
#         "key": "test_image.jpg",
#         "hash": "abc123",
#         "type": "image/jpeg"
#     }
#     create_response = await async_client.post("/images/", json=image_data)
#     image_id = create_response.json()["id"]
    
#     # Обновляем изображение
#     update_data = {
#         "article_id": article_id,
#         "key": "updated_image.jpg",
#         "hash": "xyz789",
#         "type": "image/png"
#     }
    
#     update_response = await async_client.put(f"/images/{image_id}", json=update_data)
#     assert update_response.status_code == 200
#     assert update_response.json()["key"] == update_data["key"]
#     assert update_response.json()["hash"] == update_data["hash"]
#     assert update_response.json()["type"] == update_data["type"]

# @pytest.mark.asyncio
# async def test_delete_image(async_client):
#     # Создаем тестовую категорию и статью
#     category = {"name": "Test Category"}
#     cat_response = await async_client.post("/categories/", json=category)
#     cat_id = cat_response.json()['id']
    
#     article_data = {
#         "title": "Test Article",
#         "text": "Test Text",
#         "category_id": cat_id
#     }
#     article_response = await async_client.post(
#         "/articles/",
#         data=article_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     article_id = article_response.json()["id"]
    
#     # Создаем изображение
#     image_data = {
#         "article_id": article_id,
#         "key": "test_image.jpg",
#         "hash": "abc123",
#         "type": "image/jpeg"
#     }
#     create_response = await async_client.post("/images/", json=image_data)
#     image_id = create_response.json()["id"]
    
#     # Удаляем изображение
#     delete_response = await async_client.delete(f"/images/{image_id}")
#     assert delete_response.status_code == 204
    
#     # Проверяем, что изображение удалено
#     get_response = await async_client.get(f"/images/article/{article_id}")
#     assert len(get_response.json()) == 0

# @pytest.mark.asyncio
# async def test_get_image_presigned_url(async_client):
#     # Создаем тестовую категорию и статью
#     category = {"name": "Test Category"}
#     cat_response = await async_client.post("/categories/", json=category)
#     cat_id = cat_response.json()['id']
    
#     article_data = {
#         "title": "Test Article",
#         "text": "Test Text",
#         "category_id": cat_id
#     }
#     article_response = await async_client.post(
#         "/articles/",
#         data=article_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )
#     article_id = article_response.json()["id"]
    
#     # Создаем изображение
#     image_data = {
#         "article_id": article_id,
#         "key": "test_image.jpg",
#         "hash": "abc123",
#         "type": "image/jpeg"
#     }
#     create_response = await async_client.post("/images/", json=image_data)
#     image_id = create_response.json()["id"]
    
#     # Получаем presigned URL
#     response = await async_client.get(f"/images/{image_id}/presigned-url")
#     assert response.status_code == 200
#     assert "presigned_url" in response.json()
#     assert response.json()["id"] == image_id
#     assert response.json()["key"] == image_data["key"]
#     assert response.json()["type"] == image_data["type"]
