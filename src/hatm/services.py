from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import uuid 

from logger import LOGGER
from .models import Hatm, Juz, JusStatusEnum
from .schemas import HatmCreate, JuzTakeRequest, JuzTakeResponse

class HatmService:
    @staticmethod
    def get_hatm(db: Session):
        try:
            hatms = db.query(Hatm.id, Hatm.title, Hatm.description, Hatm.is_public, Hatm.deadline).all()
            hatms_list = []
            for hatm in hatms:
                juzs = JuzService.get_juzs(db, hatm.id)
                hatms_list.append(
                    {
                        "id": hatm.id,
                        "title": hatm.title,
                        "description": hatm.description,
                        "is_public": hatm.is_public,
                        "deadline": hatm.deadline,
                        "juzs": juzs
                    }
                )
            return hatms_list
        except:
            LOGGER.exception("Error while fetching hatms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while fetching hatms")

    @staticmethod
    def create_hatm(db: Session, hatm_data: HatmCreate, user_id: UUID):
        try:
            hatm_id = uuid.uuid4()
            new_hatm = Hatm(id=hatm_id, **hatm_data.dict(), creator_id=user_id)
            db.add(new_hatm)
            db.commit()
            db.refresh(new_hatm)

            JuzService.create_juzs(db, hatm_id)
            juzs = JuzService.get_juzs(db, hatm_id)
            return {
                "id": new_hatm.id,
                "title": new_hatm.title,
                "description": new_hatm.description,
                "is_public": new_hatm.is_public,
                "deadline": new_hatm.deadline,
                "juzs": juzs
            }
        except:
            LOGGER.exception("Error while creating hatm")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while creating hatm")

    @staticmethod
    def get_users_hatms(db: Session, user_id: UUID):
        try:
            hatms = db.query(Hatm).join(Juz).filter(Juz.user_id == user_id).all()
            hatms_list = []
            for hatm in hatms:
                juzs = JuzService.get_juzs(db, hatm.id)
                hatms_list.append(
                    {
                        "id": hatm.id,
                        "title": hatm.title,
                        "description": hatm.description,
                        "is_public": hatm.is_public,
                        "deadline": hatm.deadline,
                        "juzs": juzs
                    }
                )
            return hatms_list
        except:
            LOGGER.exception("Error while fetching users hatms")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while fetching users hatms")


    @staticmethod
    def get_hatm_by_id(db: Session, hatm_id: UUID):
        try:
            hatm = db.query(Hatm).filter(Hatm.id == hatm_id).first()
            if not hatm:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hatm not found")
            juzs = JuzService.get_juzs(db, hatm_id)
            return {
                "id": hatm.id,
                "title": hatm.title,
                "description": hatm.description,
                "is_public": hatm.is_public,
                "deadline": hatm.deadline,
                "juzs": juzs
            }
        except:
            LOGGER.exception("Error while fetching hatm by id")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while fetching hatm")

    @staticmethod
    def get_hatm_juzs(db: Session, hatm_id: UUID):
        hatm = HatmService.get_hatm_by_id(db, hatm_id)
        return hatm.juzs


class JuzService:
    @staticmethod
    def get_juzs(db: Session, hatm_id: UUID):
        juzs = db.query(
            Juz.id,
            Juz.hatm_id,
            Juz.index,
            Juz.is_completed,
            Juz.deadline,
            Juz.user_id
        ).filter(Juz.hatm_id == hatm_id).all()
        juzs_list = []
        for juz in juzs:
            juzs_list.append(
                {
                    "id": juz.id,
                    "hatm_id": juz.hatm_id,
                    "juz_number": juz.index,
                    "status": "free" if not juz.user_id else "in_progress" if not juz.is_completed else "completed",
                    "type": "dua" if juz.index == 31 else "juz",
                    "deadline": juz.deadline,
                    "user_id": juz.user_id
                }
            )
        return juzs_list


    @staticmethod
    def create_juzs(db: Session, hatm_id: UUID):
        juzs = []
        for i in range(1, 32):
            juz_id = uuid.uuid4()
            juz = Juz(
                id=juz_id,
                index=i,
                hatm_id=hatm_id
            )
            juzs.append(juz)
        db.add_all(juzs)
        db.commit()
        return

    @staticmethod
    def cancel_juz(db: Session, juz_id: UUID, user_id: UUID):
        try:
            juz = db.query(Juz).filter(Juz.id == juz_id, Juz.user_id == user_id).first()
            if not juz:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Juz not found or not owned by user")
            juz.is_completed = False
            juz.user_id = None
            db.commit()
            return {
                "id": juz.id,
                "hatm_id": juz.hatm_id,
                "juz_number": juz.index,
                "status": "free" if not juz.user_id else "in_progress" if not juz.is_completed else "completed",
                "type": "dua" if juz.index == 31 else "juz",
                "deadline": juz.deadline,
                "user_id": juz.user
            }
        except:
            LOGGER.exception("Error while canceling juz")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while canceling juz")
        

    @staticmethod
    def finish_juz(db: Session, juz_id: UUID, user_id: UUID):
        try:
            juz = db.query(Juz).filter(Juz.id == juz_id, Juz.user_id == user_id).first()
            if not juz:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Juz not found or not owned by user")
            juz.is_completed = True
            db.commit()
            return {
                "id": juz.id,
                "hatm_id": juz.hatm_id,
                "juz_number": juz.index,
                "status": "free" if not juz.user_id else "in_progress" if not juz.is_completed else "completed",
                "type": "dua" if juz.index == 31 else "juz",
                "deadline": juz.deadline,
                "user_id": juz.user_id
            }
        except:
            LOGGER.exception("Error while finishing juz")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while finishing juz")

    @staticmethod
    def finish_my_juz(db: Session, user_id: UUID):
        juzs = db.query(Juz).filter(Juz.user_id == user_id, Juz.is_completed == False).all()
        for juz in juzs:
            juz.is_completed = True
        db.commit()
        return juzs

    @staticmethod
    def take_juz(db: Session, request: JuzTakeRequest, user_id: UUID):
        try:
            juzs = db.query(Juz).filter(Juz.id.in_(request.ids)).all()
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

            db.commit()
            return JuzTakeResponse(
                already_taken=already_taken,
                successfully_taken=successfully_taken,
                unsuccessfully_taken=unsuccessfully_taken,
                deadline=datetime.now() + timedelta(days=request.days)
            )
        except:
            LOGGER.exception("Error while taking juz")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while taking juz")
        

    @staticmethod
    def my_juzs(db: Session, user_id: UUID):
        try:
            juzs = db.query(Juz).filter(Juz.user_id == user_id).all()
            juzs_list = []
            for juz in juzs:
                juzs_list.append(
                    {
                        "id": juz.id,
                        "hatm_id": juz.hatm_id,
                        "juz_number": juz.index,
                        "status": "free" if not juz.user_id else "in_progress" if not juz.is_completed else "completed",
                        "type": "dua" if juz.index == 31 else "juz",
                        "deadline": juz.deadline,
                        "user_id": juz.user_id
                    }
                )
            return juzs_list
        except:
            LOGGER.exception("Error while getting my juzs")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error while getting my juzs")