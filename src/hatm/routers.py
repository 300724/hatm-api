from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from auth.models import User
from auth.routers import get_current_user
from database import get_db
from .services import HatmService, JuzService
from .schemas import *

router = APIRouter()


@router.get("/hatm", response_model=List[HatmGetResponse])
async def get_hatm(
    request: Request,
    db: Session = Depends(get_db),
):
    hatms = HatmService.get_hatm(db=db)
    return hatms


@router.post("/hatm", response_model=HatmGetResponse)
async def post_hatm(
    request: Request,
    hatm: HatmCreate,
    db: Session = Depends(get_db),
):
    hatm = HatmService.create_hatm(db=db, hatm_data=hatm, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0') # this user id just for example, we should create users auth endpoint and user validation
    return hatm


@router.get("/hatm/mine", response_model=List[HatmGetResponse])
async def get_my_hatm(
    request: Request,
    db: Session = Depends(get_db)
):
    hatms = HatmService.get_users_hatms(db, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0')
    return hatms


@router.get("/hatm/{hatm_id}", response_model=HatmGetResponse)
async def get_hatm_by_id(
    request: Request,
    hatm_id: UUID,
    db: Session = Depends(get_db),
):
    hatm = HatmService.get_hatm_by_id(db, hatm_id)
    return hatm


@router.get("/hatm/{hatm_id}/juzs")
async def get_hatm_juzs(
    request: Request,
    hatm_id: UUID,
    db: Session = Depends(get_db),
):
    juzs = JuzService.get_juzs(db, hatm_id)
    return juzs


@router.patch("/juzs/cancel/{juz_id}", response_model=JuzBase)
async def cancel_juz(
    request: Request,
    juz_id: UUID,
    db: Session = Depends(get_db)
):
    juz = JuzService.cancel_juz(db, juz_id, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0')
    return juz


@router.patch("/juzs/finish/{juz_id}", response_model=JuzBase)
async def finish_juz(
    request: Request,
    juz_id: UUID,
    db: Session = Depends(get_db)
):
    juz = JuzService.finish_juz(db, juz_id, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0')
    return juz


@router.patch("/juzs/take", response_model=JuzTakeResponse)
async def take_juz(
    request: Request,
    data: JuzTakeRequest,
    db: Session = Depends(get_db)
):
    juzs = JuzService.take_juz(db, data, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0')
    return juzs


@router.get("/juzs/mine", response_model=List[JuzBase])
async def my_juzs(
    request: Request,
    db: Session = Depends(get_db)
):
    juzs = JuzService.my_juzs(db, user_id='69d309bc-1bd4-41f4-974b-ce39df7223b0')
    return juzs