from src.app.services.image import ImageService
from fastapi import APIRouter, Depends, File, UploadFile, Form
from typing import Annotated
from src.app.dependencies.image import get_image_service

router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/by_article_id/{article_id}")
async def get_images_by_article_id(
    image_service: Annotated[ImageService, Depends(get_image_service)],
    article_id: int,
):
    return await image_service.get_images_by_article_id(article_id)


@router.get("/by_id/{image_id}")
async def get_image_by_id(
    image_service: Annotated[ImageService, Depends(get_image_service)],
    image_id: int,
):
    return await image_service.get_image_by_id(image_id)




@router.post("/")
async def upload_image(
    image_service: Annotated[ImageService, Depends(get_image_service)],
    article_id: int,
    type: str = Form(...),
    file: UploadFile = File(...),
):
    return await image_service.upload_image(article_id, file, type)


@router.delete("/")
async def delete_image(
    image_service: Annotated[ImageService, Depends(get_image_service)],
    image_id: int,
):
    return await image_service.delete_image(image_id)
