from datetime import datetime

from hatm.domain.models import Hatm, Juz, JuzStatus
from hatm.domain.repositories import (AbstractHatmRepository,
                                      AbstractJuzRepository)


class SQLAlchemyHatmRepository(AbstractHatmRepository):
    def __init__(self, session):
        self._session = session

    def get(self, hatm_id: str) -> Hatm:
        return self._session.query(Hatm).filter_by(id=hatm_id).first()

    def list(
        self,
        creator_id: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
    ) -> list[Hatm]:
        query = self._session.query(Hatm)
        if creator_id:
            query = query.filter_by(creator_id=creator_id)
        if is_public is not None:
            query = query.filter_by(is_public=is_public)
        if is_completed is not None:
            query = query.filter_by(is_completed=is_completed)
        if is_published is not None:
            query = query.filter_by(is_published=is_published)
        return query.all()

    def create(
        self,
        creator_id: str,
        title: str,
        description: str,
        is_public: bool,
        deadline: datetime,
    ) -> Hatm:
        hatm = Hatm(
            creator_id=creator_id,
            title=title,
            description=description,
            is_public=is_public,
            deadline=deadline,
        )
        self._session.add(hatm)
        self._session.commit()
        return hatm

    def update(
        self,
        hatm_id: str,
        title: str = None,
        description: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
        deadline: datetime = None,
    ) -> Hatm:
        hatm = self._session.query(Hatm).filter_by(id=hatm_id).first()
        if title is not None:
            hatm.title = title
        if description is not None:
            hatm.description = description
        if is_public is not None:
            hatm.is_public = is_public
        if is_completed is not None:
            hatm.is_completed = is_completed
        if is_published is not None:
            hatm.is_published = is_published
        if deadline is not None:
            hatm.deadline = deadline
        self._session.commit()
        return hatm

    def delete(self, hatm_id: str) -> None:
        hatm = self._session.query(Hatm).filter_by(id=hatm_id).first()
        self._session.delete(hatm)
        self._session.commit()


class SQLAlchemyJuzRepository(AbstractJuzRepository):
    def __init__(self, session):
        self._session = session

    def get(self, juz_id: str) -> Juz:
        return self._session.query(Juz).filter_by(id=juz_id).first()

    def list(
        self, hatm_id: str = None, user_id: str = None, status: JuzStatus = None
    ) -> list[Juz]:
        query = self._session.query(Juz)
        if hatm_id:
            query = query.filter_by(hatm_id=hatm_id)
        if user_id:
            query = query.filter_by(user_id=user_id)
        if status:
            query = query.filter_by(status=status)
        return query.all()

    def create(
        self,
        hatm_id: str,
        user_id: str,
        juz_number: int,
        status: JuzStatus,
        deadline: datetime,
    ) -> Juz:
        juz = Juz(
            hatm_id=hatm_id,
            user_id=user_id,
            juz_number=juz_number,
            status=status,
            deadline=deadline,
        )
        self._session.add(juz)
        self._session.commit()
        return juz

    def update(
        self, juz_id: str, status: JuzStatus = None, deadline: datetime = None
    ) -> Juz:
        juz = self._session.query(Juz).filter_by(id=juz_id).first()
        if status is not None:
            juz.status = status
        if deadline is not None:
            juz.deadline = deadline
        self._session.commit()
        return juz

    def delete(self, juz_id: str) -> None:
        juz = self._session.query(Juz).filter_by(id=juz_id).first()
        self._session.delete(juz)
        self._session.commit()
