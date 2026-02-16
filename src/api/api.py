from fastapi import APIRouter

from src.api.routers.player_search_router import router as player_router
from src.api.routers.rank_router import router as rank_router
from src.api.routers.stats_boost_router import router as boost_stats_router
from src.api.routers.stats_core_router import router as core_stats_router
from src.api.routers.stats_movement_router import router as movement_stats_router
from src.api.routers.stats_positionning_router import (
    router as positionning_stats_router,
)


api_router = APIRouter(prefix="/api")

api_router.include_router(player_router)
api_router.include_router(rank_router)
api_router.include_router(core_stats_router)
api_router.include_router(boost_stats_router)
api_router.include_router(movement_stats_router)
api_router.include_router(positionning_stats_router)


# Export explicite
__all__ = ["api_router"]
