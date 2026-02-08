from fastapi import APIRouter


router = APIRouter(prefix="/log_in", tags=["Log in"])


@router.post("/token", tags=["Log in"])
def testing(id: int | None = None):
    pass
