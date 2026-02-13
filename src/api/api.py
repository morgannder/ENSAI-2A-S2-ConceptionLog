from fastapi import APIRouter

from src.api.routers.global_stats_router import router as global_stats_router
from src.api.routers.player_search_router import router as player_router
from src.api.routers.rank_router import router as rank_router


# from src.api.routers import login_router

api_router = APIRouter(prefix="/api")

# api_router.include_router(login_router)
api_router.include_router(rank_router)
api_router.include_router(global_stats_router)
api_router.include_router(player_router)
# Export explicite

__all__ = ["api_router"]
