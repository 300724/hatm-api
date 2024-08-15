import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from logger import LOGGER

from .models import Hatm, Juz
from .schemas import HatmCreate, JuzTakeRequest, JuzTakeResponse


class JuzService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_juzs(self, hatm_id: str) -> list[dict]:
        juzs = (
            self._session.query(
                Juz.id,
                Juz.hatm_id,
                Juz.index,
                Juz.is_completed,
                Juz.deadline,
                Juz.user_id,
            )
            .filter(Juz.hatm_id == hatm_id)
            .all()
        )

        return [
            {
                "id": juz.id,
                "hatm_id": juz.hatm_id,
                "juz_number": juz.index,
                "status": self._get_juz_status(juz),
                "type": "dua" if juz.index == 31 else "juz",
                "deadline": juz.deadline,
                "user_id": juz.user_id,
            }
            for juz in juzs
        ]

    def create_juzs(self, hatm_id: str) -> None:
        juzs = [Juz(id=uuid.uuid4(), index=i, hatm_id=hatm_id) for i in range(1, 32)]
        self._session.add_all(juzs)
        self._session.commit()

    def cancel_juz(self, juz_id: str, user_id: str) -> dict:
        try:
            juz = self._get_user_owned_juz(juz_id, user_id)
            juz.user_id = None
            juz.deadline = None
            juz.is_completed = False
            self._session.commit()
            return self._get_juz_dict(juz)
        except HTTPException as e:
            self._handle_exception("Juz not found or not owned by user", e)
        except SQLAlchemyError as e:
            self._handle_exception("Error while canceling juz", e)

    def finish_juz(self, juz_id: str, user_id: str) -> dict:
        try:
            juz = self._get_user_owned_juz(juz_id, user_id)
            juz.is_completed = True
            self._session.commit()
            return self._get_juz_dict(juz)
        except HTTPException as e:
            self._handle_exception("Juz not found or not owned by user", e)
        except SQLAlchemyError as e:
            self._handle_exception("Error while finishing juz", e)

    def finish_my_juz(self, user_id: str) -> list[Juz]:
        juzs = (
            self._session.query(Juz)
            .filter(Juz.user_id == user_id, Juz.is_completed is False)
            .all()
        )
        for juz in juzs:
            juz.is_completed = True
        self._session.commit()
        return juzs

    def take_juz(self, request: JuzTakeRequest, user_id: str) -> JuzTakeResponse:
        try:
            juzs = self._session.query(Juz).filter(Juz.id.in_(request.ids)).all()
            already_taken = []
            successfully_taken = []
            unsuccessfully_taken = []

            for juz in juzs:
                if juz.user_id:
                    already_taken.append(juz.index)
                else:
                    if juz.deadline and juz.deadline < datetime.now():
                        unsuccessfully_taken.append(juz.index)
                    else:
                        juz.user_id = user_id
                        juz.deadline = datetime.now() + timedelta(days=request.days)
                        successfully_taken.append(juz.index)

            self._session.commit()
            return JuzTakeResponse(
                already_taken=already_taken,
                successfully_taken=successfully_taken,
                unsuccessfully_taken=unsuccessfully_taken,
                deadline=datetime.now() + timedelta(days=request.days),
            )
        except SQLAlchemyError as e:
            self._handle_exception("Error while taking juz", e)

    def my_juzs(self, user_id: str) -> list[dict]:
        try:
            juzs = self._session.query(Juz).filter(Juz.user_id == user_id).all()
            return [self._get_juz_dict(juz) for juz in juzs]
        except SQLAlchemyError as e:
            self._handle_exception("Error while getting my juzs", e)

    def _get_user_owned_juz(self, juz_id: str, user_id: str) -> Juz:
        return (
            self._session.query(Juz)
            .filter(Juz.id == juz_id, Juz.user_id == user_id)
            .first()
        )

    def _get_juz_status(self, juz: Juz) -> str:
        if not juz.user_id:
            return "free"
        return "in_progress" if not juz.is_completed else "completed"

    def _get_juz_dict(self, juz: Juz) -> dict:
        return {
            "id": juz.id,
            "hatm_id": juz.hatm_id,
            "juz_number": juz.index,
            "status": self._get_juz_status(juz),
            "type": "dua" if juz.index == 31 else "juz",
            "deadline": juz.deadline,
            "user_id": juz.user_id,
        }

    def _handle_exception(self, message: str, exception: Exception) -> None:
        LOGGER.exception(f"{message}: {str(exception)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )


class HatmService:
    def __init__(self, session: Session, juz_service: JuzService) -> None:
        self._session = session
        self._juz_service = juz_service

    def get_all_hatms(self) -> list[dict]:
        try:
            hatms = self._session.query(
                Hatm.id, Hatm.title, Hatm.description, Hatm.is_public, Hatm.deadline
            ).all()
            return [self._build_hatm_dict(hatm) for hatm in hatms]
        except Exception as e:
            self._handle_exception("Error while fetching hatms", e)

    def create_hatm(self, hatm_data: HatmCreate, user_id: str) -> dict:
        try:
            hatm_id = uuid.uuid4()
            new_hatm = Hatm(id=hatm_id, **hatm_data.model_dump(), creator_id=user_id)
            self._session.add(new_hatm)
            self._session.commit()
            self._session.refresh(new_hatm)

            self._juz_service.create_juzs(hatm_id)
            juzs = self._juz_service.get_juzs(hatm_id)
            return self._build_hatm_dict(new_hatm, juzs)
        except Exception as e:
            self._handle_exception("Error while creating hatm", e)

    def get_users_hatms(self, user_id: str) -> list[dict]:
        try:
            hatms = (
                self._session.query(Hatm).join(Juz).filter(Juz.user_id == user_id).all()
            )
            return [self._build_hatm_dict(hatm) for hatm in hatms]
        except Exception as e:
            self._handle_exception("Error while fetching users hatms", e)

    def get_hatm_by_id(self, hatm_id: str) -> dict:
        try:
            hatm = self._session.query(Hatm).filter(Hatm.id == hatm_id).first()
            juzs = self._juz_service.get_juzs(hatm_id)
            return self._build_hatm_dict(hatm, juzs)
        except HTTPException as e:
            self._handle_exception("Hatm not found", e)
        except Exception as e:
            self._handle_exception("Error while fetching hatm by id", e)

    def get_hatm_juzs(self, hatm_id: str):
        print(hatm_id)

    def _build_hatm_dict(self, hatm: Hatm, juzs: list[dict] = None) -> dict:
        hatm_dict = {
            "id": hatm.id,
            "title": hatm.title,
            "description": hatm.description,
            "is_public": hatm.is_public,
            "deadline": hatm.deadline,
        }
        if juzs:
            hatm_dict["juzs"] = juzs
        return hatm_dict

    def _handle_exception(self, message: str, exception: Exception) -> None:
        LOGGER.exception(f"{message}: {str(exception)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
