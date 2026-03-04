from fastapi import APIRouter, HTTPException, status

from src.api.schemas.stats_response import MatchResponse
from src.dto.match_players_dto import MatchPlayersDTO
from src.service.matches_service import MatchService


router = APIRouter(prefix="/match", tags=["Matches"])

match_service = MatchService()


@router.get(
    "/match-players/",
    response_model=MatchPlayersDTO,
    summary="Extract players from a match using match ID",
    description="Renvoie l'ensemble des joueurs participant à un match en utilisant"
    "l'id de ce match. Contient les infos complètes des joueurs triés par équipe.",
)
def match_players(match_id: int | None = None):
    if not match_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le paramètre match_id est requis.",
        )

    try:
        players_dto = match_service.get_match_players(match_id)

        if players_dto is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun joueur trouvé pour le match avec l'id : {match_id}",
            )

        return players_dto

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}",
        ) from e


@router.get(
    "/by-match-team/{match_team_id}",
    response_model=MatchResponse,
    summary="Extract match information using match_team ID",
    description="Renvoie les informations d'un match à partir de l'id d'un match_team",
)
def get_match_by_match_team_id(match_team_id: int | None = None):
    if not match_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le paramètre match_team_id est requis.",
        )
    try:
        match = match_service.get_match_by_match_team_id(match_team_id)

        if match is None:
            raise HTTPException(status_code=404, detail="Match not found")

        return match

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur interne du serveur: {str(e)}",
        ) from e
