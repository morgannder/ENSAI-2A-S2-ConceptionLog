from fastapi import APIRouter

from .routers import login


api_router = APIRouter()

api_router.include_router(login.router, prefix="/log_in", tags=["Log in"])
# api_router.include_router(users.router, prefix="/my_account", tags=["User"])
# api_router.include_router(Les autres routers à rajouter)

# Export explicite
__all__ = ["api_router"]
