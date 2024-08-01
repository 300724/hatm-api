from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from hatm.application.repositories import (SQLAlchemyHatmRepository,
                                           SQLAlchemyJuzRepository)
from hatm.application.services import HatmService, JuzService
from hatm.domain.models import Hatm, Juz, JuzStatus
from hatm.infrastructure.request_models import (CreateHatmRequest,
                                                CreateJuzRequest,
                                                UpdateHatmRequest,
                                                UpdateJuzRequest)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()


def get_hatm_service(session: Session = Depends(get_db)):
    hatm_repository = SQLAlchemyHatmRepository(session)
    return HatmService(hatm_repository)


def get_juz_service(session: Session = Depends(get_db)):
    juz_repository = SQLAlchemyJuzRepository(session)
    return JuzService(juz_repository)


hatm_router = APIRouter(prefix="/hatm", tags=["Hatm"])
juz_router = APIRouter(prefix="/juz", tags=["Juz"])


@hatm_router.get("/{hatm_id}", response_model=Hatm)
def get_hatm(hatm_id: str, service: HatmService = Depends(get_hatm_service)):
    hatm = service.get_hatm(hatm_id)
    if not hatm:
        raise HTTPException(status_code=404, detail="Hatm not found")
    return hatm


@hatm_router.get("/", response_model=list[Hatm])
def list_hatms(
    creator_id: str = None,
    is_public: bool = None,
    is_completed: bool = None,
    is_published: bool = None,
    service: HatmService = Depends(get_hatm_service),
):
    hatms = service.list_hatms(creator_id, is_public, is_completed, is_published)
    return hatms


@hatm_router.post("/", response_model=Hatm)
def create_hatm(
    request: CreateHatmRequest, service: HatmService = Depends(get_hatm_service)
):
    hatm = service.create_hatm(
        request.creator_id,
        request.title,
        request.description,
        request.is_public,
        request.deadline,
    )
    return hatm


@hatm_router.put("/{hatm_id}", response_model=Hatm)
def update_hatm(
    hatm_id: str,
    request: UpdateHatmRequest,
    service: HatmService = Depends(get_hatm_service),
):
    hatm = service.update_hatm(
        hatm_id,
        request.title,
        request.description,
        request.is_public,
        request.is_completed,
        request.is_published,
        request.deadline,
    )
    if not hatm:
        raise HTTPException(status_code=404, detail="Hatm not found")
    return hatm


@hatm_router.delete("/{hatm_id}", status_code=204)
def delete_hatm(hatm_id: str, service: HatmService = Depends(get_hatm_service)):
    service.delete_hatm(hatm_id)


@juz_router.get("/{juz_id}", response_model=Juz)
def get_juz(juz_id: str, service: JuzService = Depends(get_juz_service)):
    juz = service.get_juz(juz_id)
    if not juz:
        raise HTTPException(status_code=404, detail="Juz not found")
    return juz


@juz_router.get("/", response_model=list[Juz])
def list_juzs(
    hatm_id: str = None,
    user_id: str = None,
    status: JuzStatus = None,
    service: JuzService = Depends(get_juz_service),
):
    juzs = service.list_juzs(hatm_id, user_id, status)
    return juzs


@juz_router.post("/", response_model=Juz)
def create_juz(
    request: CreateJuzRequest, service: JuzService = Depends(get_juz_service)
):
    juz = service.create_juz(
        request.hatm_id,
        request.user_id,
        request.juz_number,
        request.status,
        request.deadline,
    )
    return juz


@juz_router.put("/{juz_id}", response_model=Juz)
def update_juz(
    juz_id: str,
    request: UpdateJuzRequest,
    service: JuzService = Depends(get_juz_service),
):
    juz = service.update_juz(juz_id, request.status, request.deadline)
    if not juz:
        raise HTTPException(status_code=404, detail="Juz not found")
    return juz


@juz_router.delete("/{juz_id}", status_code=204)
def delete_juz(juz_id: str, service: JuzService = Depends(get_juz_service)):
    service.delete_juz(juz_id)
