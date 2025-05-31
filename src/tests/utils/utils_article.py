async def create_test_category(async_client, category_data: dict):
    response = await async_client.post("/categories/", json=category_data)
    return response

async def create_test_article(
        async_client, 
        category_data: dict, 
        article_data: dict
):
    category_response = await create_test_category(
        async_client=async_client, 
        category_data=category_data
    )
    print(category_response.json())
    article_data['category_id'] = category_response.json()['id']

    response = await async_client.post("/articles/", data=article_data)
    return response

async def get_test_articles(
        async_client, 
        categories_data: dict, 
        articles_data: dict
):
    for category_data, article_data in zip(categories_data, articles_data):
        await create_test_article(
            async_client, 
            category_data, 
            article_data
        )

    response = await async_client.get("/articles/")
    return response

async def update_test_article(
        async_client, 
        category_data: dict, 
        article_data: dict,
        article_update_data: dict
):
    article_response = await create_test_article(
            async_client, 
            category_data, 
            article_data
    )
    article_id = article_response.json()['id']
    response = await async_client.put(f"/articles/{article_id}", data=article_update_data)
    return response

async def soft_delete_test_article(
        async_client, 
        category_data: dict, 
        article_data: dict
):
    article_response = await create_test_article(
        async_client, 
        category_data, 
        article_data
    )
    article_id = article_response.json()['id']
    response = await async_client.delete(f"/articles/{article_id}")
    return response