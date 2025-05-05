from fastapi import APIRouter, UploadFile, File, status, Query, Depends, Path
from src.app.services.s3 import S3Service
from src.app.dependencies.s3 import get_s3_service

router = APIRouter(prefix="/s3", tags=["s3"])

@router.post("/upload/", status_code=status.HTTP_201_CREATED)
async def upload(
    file: UploadFile = File(...),
    s3_service: S3Service = Depends(get_s3_service)
):
    key = f"uploads/{file.filename}"
    url = await s3_service.upload_file(file.file, key, file.content_type)
    return {"url": url, "key": key}

@router.delete("/delete/", status_code=status.HTTP_200_OK)
async def delete(
    key: str = Query(..., description="S3 object key"),
    s3_service: S3Service = Depends(get_s3_service)
):
    await s3_service.delete_file(key)
    return {"deleted_key": key}

@router.get("/presigned/{key}", status_code=status.HTTP_200_OK)
async def generate_presigned_url(
    key: str,
    s3_service: S3Service = Depends(get_s3_service)
):
    url = await s3_service.generate_presigned_url(key)
    return url

@router.get("/list/", status_code=status.HTTP_200_OK)
async def list_all(
    s3_service: S3Service = Depends(get_s3_service)
):
    return {"files": await s3_service.list_files()} 