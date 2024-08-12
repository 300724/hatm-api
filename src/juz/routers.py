from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.models import User
from auth.routers import get_current_user
from database import get_db

from .schemas import Juz, Message, TakeJuz, TakeJuzResponse

router = APIRouter()


@router.post("/take", response_model=TakeJuzResponse)
async def take_juzs(
    juzDto: TakeJuz,
    db: Session = Depends(get_db),
):
    print(juzDto, db)


@router.get("/mine", response_model=list[Juz])
async def get_my_juzs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)


@router.patch("/cancel/{id}", response_model=Message)
async def cancel_juz(
    request: Request,
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """This route takes a list of juz ids and cancels them. It returns a list of juz numbers that were already cancelled and a list of juz numbers that were succesfully cancelled."""
    print(request, db, id, current_user)


@router.patch("/finish/{id}", response_model=Message)
async def finish_juz(
    request: Request,
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """This route takes a list of juz ids and finishes them. It returns a list of juz numbers that were already finished and a list of juz numbers that were succesfully finished."""
    print(request, id, db, current_user)
