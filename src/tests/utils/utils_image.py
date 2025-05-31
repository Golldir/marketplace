from pathlib import Path
from src.tests.utils.utils_article import create_test_article

async def create_test_image(async_client, category_data, article_data):

	article_response = await create_test_article(
		async_client,
		category_data=category_data,
		article_data=article_data
	)
	article_id = article_response.json()['id']
	print('article_id', article_id)

	image_path = Path("src/tests/utils/test_image.jpg")
	with open(image_path, "rb") as f:
		response = await async_client.post(
			"/images/", 
			data={"type": "content", 'article_id': article_id}, 
			files={"file": ("filename", f, "image/jpeg")}
		)
	return response

async def get_test_image(
		async_client, 
		category_data, 
		article_data
):
	image_response = await create_test_image(
		async_client, 
		category_data=category_data, 
		article_data=article_data
	)

	response = await async_client.get(f"/images/by_article_id/{image_response.json()['article_id']}")
	return response

async def delete_test_image(async_client, category_data, article_data):
	image_response = await create_test_image(
		async_client, 
		category_data=category_data, 
		article_data=article_data
	)
	print('image_response', image_response.json())
	image_id = image_response.json()['id']
	response = await async_client.delete("/images/", params={"image_id": image_id})
	return response
