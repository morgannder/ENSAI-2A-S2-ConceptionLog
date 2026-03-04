from fastapi import APIRouter, HTTPException, status

from src.dto.match_team_dto import MatchTeamResponseDTO
from src.service.match_teams_service import MatchTeamService


router = APIRouter(prefix="/match_team", tags=["Match Teams"])

match_team_service = MatchTeamService()


@router.get(
    "/team/{match_team_id}",
    response_model=MatchTeamResponseDTO,
    summary="Extract match_team information using match_team ID",
    description="Renvoie les informations d'un match_team à partir de son id",
)
def get_match_team_by_id(match_team_id: int):
    if not match_team_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le paramètre match_team_id est requis.",
        )
    try:
        match = match_team_service.get_match_team_by_id(match_team_id)

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


@router.get(
    "/match/{match_id}",
    response_model=list[MatchTeamResponseDTO],
    summary="Extract 2 match_team using match ID",
    description="Renvoie les informations des 2 match_team correspondant à un match",
)
def get_match_team_by_match_id(match_id: str):
    if not match_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Le paramètre match_id est requis.",
        )
    try:
        match = match_team_service.get_teams_by_match(match_id)

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
