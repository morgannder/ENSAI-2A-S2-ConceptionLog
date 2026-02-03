from environment_printer import EnvironmentPrinter
from fastapi import FastAPI
from src.api.api import api_router
from src.api.core.config import settings
import uvicorn

app = FastAPI(title="RocketCL API", description="API de gestion de suivi de parties sur le jeu Rocket League", version=settings.APP_VERSION
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=(settings.ENVIRONNEMENT == "development") 
    )
