from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.models import User
from auth.routers import get_current_user
from database import get_db
from juz.schemas import Juz

from .schemas import HatmCreate, HatmGet

router = APIRouter()


@router.post("", response_model=HatmGet)
async def create_hatm(
    hatmDto: HatmCreate,
):
    print(hatmDto)


@router.get("", response_model=list[HatmGet])
async def get_hatm(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)


@router.get("/mine", response_model=list[HatmGet])
async def get_my_hatm(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, db, current_user)


@router.get("/{hatm_id}", response_model=HatmGet)
async def get_hatm_by_id(
    request: Request,
    hatm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, hatm_id, db, current_user)


@router.get("/{hatm_id}/juzs", response_model=list[Juz])
async def get_free_juzs_of_hatm(
    request: Request,
    hatm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print(request, hatm_id, db, current_user)
