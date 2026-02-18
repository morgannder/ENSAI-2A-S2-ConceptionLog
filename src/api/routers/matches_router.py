from fastapi import APIRouter

from src.service.matches_service import MatchService


router = APIRouter(prefix="/match", tags=["Matches"])

match_service = MatchService()
