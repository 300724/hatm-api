from uuid import UUID

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from src.database import get_db

from src.hatm.schemas import (HatmCreate, HatmGetResponse, JuzBase, JuzTakeRequest,
                      JuzTakeResponse)
from src.hatm.services import HatmService, JuzService

router = APIRouter()


@router.get("/hatm", response_model=list[HatmGetResponse])
async def get_hatm(db: Session = Depends(get_db)):
    hatm_service = HatmService(db, JuzService(db))
    return hatm_service.get_all_hatms()


@router.post("/hatm", response_model=HatmGetResponse)
async def post_hatm(
    request: Request,
    hatm: HatmCreate,
    db: Session = Depends(get_db),
):
    user_id = f"my user_id taken from {request}"
    hatm_service = HatmService(db, JuzService(db))
    return hatm_service.create_hatm(hatm, user_id)


@router.get("/hatm/mine", response_model=list[HatmGetResponse])
async def get_my_hatm(request: Request, db: Session = Depends(get_db)):
    user_id = f"my user_id taken from {request}"
    hatm_service = HatmService(db, JuzService(db))
    return hatm_service.get_users_hatms(user_id)


@router.get("/hatm/{hatm_id}", response_model=HatmGetResponse)
async def get_hatm_by_id(
    hatm_id: UUID,
    db: Session = Depends(get_db),
):
    hatm_service = HatmService(db, JuzService(db))
    return hatm_service.get_hatm_by_id(hatm_id)


@router.get("/hatm/{hatm_id}/juzs")
async def get_hatm_juzs(
    hatm_id: UUID,
    db: Session = Depends(get_db),
):
    hatm_service = HatmService(db, JuzService(db))
    return hatm_service.get_hatm_juzs(hatm_id)


@router.patch("/juzs/cancel/{juz_id}", response_model=JuzBase)
async def cancel_juz(request: Request, juz_id: UUID, db: Session = Depends(get_db)):
    user_id = f"my user_id taken from {request}"
    juz_service = JuzService(db)
    return juz_service.cancel_juz(juz_id, user_id)


@router.patch("/juzs/finish/{juz_id}", response_model=JuzBase)
async def finish_juz(request: Request, juz_id: UUID, db: Session = Depends(get_db)):
    user_id = f"my user_id taken from {request}"
    juz_service = JuzService(db)
    return juz_service.finish_juz(juz_id, user_id)


@router.patch("/juzs/take", response_model=JuzTakeResponse)
async def take_juz(
    request: Request, data: JuzTakeRequest, db: Session = Depends(get_db)
):
    user_id = f"my user_id taken from {request}"
    juz_service = JuzService(db)
    return juz_service.take_juz(data, user_id)


@router.get("/juzs/mine", response_model=list[JuzBase])
async def my_juzs(request: Request, db: Session = Depends(get_db)):
    user_id = f"my user_id taken from {request}"
    juz_service = JuzService(db)
    return juz_service.my_juzs(user_id)
