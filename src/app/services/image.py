from src.app.repositories.image import ImageRepository
from fastapi import UploadFile, HTTPException
from src.app.services.utils import generate_file_key, generate_file_hash
from src.app.schemas.image import ImageCreateSchema, ImageGetSchema
from src.app.repositories.s3 import S3Repository
from typing import List

class ImageService:
    def __init__(
            self, 
            image_repository: ImageRepository, 
            s3_repository: S3Repository
    ):
        self.image_repository = image_repository
        self.s3_repository = s3_repository

    async def get_images_by_article_id(self, article_id: int) -> List[ImageGetSchema]:
        images = await self.image_repository.get_images_by_article_id(article_id)
        if not images:
            raise HTTPException(status_code=404, detail="Images not found")
        
        return images

    async def get_image_by_id(self, image_id: int) -> ImageGetSchema:
        image = await self.image_repository.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image

    async def upload_image(self, article_id: int, file: UploadFile, type: str) -> str:
        key = generate_file_key(file.filename)
        hash = await generate_file_hash(file)

        hash_exists = await self.image_repository.get_image_by_hash(hash)
        if hash_exists:
            raise HTTPException(status_code=400, detail="Image with this hash already exists")

        image_create_schema = ImageCreateSchema(
            article_id=article_id,
            key=key,
            hash=hash,
            type=type
        )

        await self.s3_repository.upload_fileobj(file, key)
        return await self.image_repository.create_image(image_create_schema)
    
    async def delete_image(self, image_id: int) -> dict:
        image = await self.image_repository.get_image_by_id(image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        
        await self.s3_repository.delete_object(image.key)
        await self.image_repository.delete_image(image_id)
        # TODO изменить return 
        return {"message": "Image deleted successfully"}
