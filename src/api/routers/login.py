from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


router = APIRouter(tags=["Log in"])

@router.post("/token", tags=["Log in"])
def testing(id: Optional[int]=None):
    pass