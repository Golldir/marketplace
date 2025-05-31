import pytest
from src.tests.utils.utils_category import (
    create_test_category,
    get_test_categories,
    update_test_category,
    soft_delete_test_category
)
from src.tests.fixtures.test_data import (
    test_categories_data,
    test_category_update_data
)

@pytest.mark.asyncio
async def test_main(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Привет, мир!"}

@pytest.mark.asyncio
async def test_create_category(async_client):
    response = await create_test_category(
        async_client=async_client, 
        category_data=test_categories_data[0]
    )

    assert response.status_code == 201
    assert response.json()['name'] == test_categories_data[0]['name']

@pytest.mark.asyncio
async def test_get_category(async_client):
    response = await get_test_categories(
        async_client=async_client, 
        categories_data=test_categories_data
    )
    for i in zip(response.json(), test_categories_data):
        assert i[0]['name'] == i[1]['name']
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_category(async_client):
    response = await update_test_category(
        async_client=async_client,
        category_data=test_categories_data[0],
        category_update_data=test_category_update_data
    )
    assert response.status_code == 200
    assert response.json()['name'] == test_category_update_data['name']

@pytest.mark.asyncio
async def test_delete_category(async_client):
    response = await soft_delete_test_category(
        async_client=async_client,
        category_data=test_categories_data[0]
    )
    assert response.status_code == 200