from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.models import User
from auth.routers import get_current_user
from database import get_db

router = APIRouter()


@router.post("/take")
async def take_juzs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)


@router.get("/mine")
async def get_my_juzs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)


@router.patch("/cancel/{id}")
async def cancel_juz(
    request: Request,
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """This route takes a list of juz ids and cancels them. It returns a list of juz numbers that were already cancelled and a list of juz numbers that were succesfully cancelled."""
    print(request, id, db, current_user)
    
@router.patch("/finish/{id}")
async def finish_juz(
    request: Request,
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """This route takes a list of juz ids and finishes them. It returns a list of juz numbers that were already finished and a list of juz numbers that were succesfully finished."""
    print(request, id, db, current_user)