import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Ajout de l'import
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

origins = [
    "http://rocketclstats.api.kub.sspcloud.fr",
    "https://rocketclstats.api.kub.sspcloud.fr",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
