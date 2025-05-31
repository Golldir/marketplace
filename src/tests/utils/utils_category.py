async def create_test_category(async_client, category_data: dict):
    response = await async_client.post("/categories/", json=category_data)
    return response

async def get_test_categories(async_client, categories_data: dict):
    for category_data in categories_data:
        await create_test_category(async_client, category_data)

    response = await async_client.get("/categories/")
    return response

async def update_test_category(
        async_client, 
        category_data: dict, 
        category_update_data: dict
):
    category_response = await create_test_category(
        async_client=async_client,
        category_data=category_data
    )
    category_id = category_response.json()['id']
    response = await async_client.put(f"/categories/{category_id}", json=category_update_data)
    return response

async def soft_delete_test_category(
        async_client, 
        category_data: dict
):
    category_response = await create_test_category(
        async_client=async_client,
        category_data=category_data
    )
    category_id = category_response.json()['id']
    response = await async_client.delete(f"/categories/{category_id}")
    return response