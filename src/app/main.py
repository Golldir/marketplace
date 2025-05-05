from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.app.routers.category import router as category_router
from src.app.routers.s3 import router as s3_router
from src.app.routers.article import router as article_router
from src.app.routers.image import router as image_router


# TODO skip спросить про обработку ошибок
# TODO в core спросить про сессии и клиентов?

app = FastAPI(
    title="Blog API",
    description="API для блога с категориями статей",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.include_router(category_router)
app.include_router(s3_router)
app.include_router(article_router)
app.include_router(image_router)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():   
    return {"message": "Привет, мир!"}
