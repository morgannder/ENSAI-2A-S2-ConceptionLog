from fastapi import APIRouter

from api.routers import login, users


# Création du routeur principal
api_router = APIRouter()

# Inclusion des routeurs
api_router.include_router(login.router, prefix="/log_in", tags=["Log in"])
api_router.include_router(users.router, prefix="/my_account", tags=["User"])

# Export explicite
__all__ = ["api_router"]
