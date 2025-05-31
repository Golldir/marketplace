from fastapi import UploadFile
from pathlib import Path
from io import BytesIO
from src.tests.utils.utils_article import create_test_article
from src.tests.fixtures.test_data import test_categories_data, test_articles_data

async def create_test_image(async_client):

	article_response = await create_test_article(
		async_client,
		category_data=test_categories_data[0],
		article_data=test_articles_data[0]
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

