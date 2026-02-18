import os

from fastapi import FastAPI
import uvicorn

from src.api.api import api_router
from src.api.core.config import settings


app = FastAPI(
    title="RocketCL API",
    description="API de gestion de suivi de parties sur le jeu Rocket League",
    version=settings.APP_VERSION,
    docs_url="/",
    redoc_url=None,
)

app.include_router(api_router)

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    uvicorn.run(
        "main:app",
        host=host,
        port=8000,
        reload=(settings.ENVIRONNEMENT == "development"),
    )
