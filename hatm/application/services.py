from datetime import datetime

from hatm.domain.models import Hatm, Juz, JuzStatus
from hatm.domain.repositories import (AbstractHatmRepository,
                                      AbstractJuzRepository)


class HatmService:
    def __init__(self, hatm_repository: AbstractHatmRepository):
        self._hatm_repository = hatm_repository

    def get_hatm(self, hatm_id: str) -> Hatm:
        return self._hatm_repository.get(hatm_id)

    def list_hatms(
        self,
        creator_id: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
    ) -> list[Hatm]:
        return self._hatm_repository.list(
            creator_id, is_public, is_completed, is_published
        )

    def create_hatm(
        self,
        creator_id: str,
        title: str,
        description: str,
        is_public: bool,
        deadline: datetime,
    ) -> Hatm:
        return self._hatm_repository.create(
            creator_id, title, description, is_public, deadline
        )

    def update_hatm(
        self,
        hatm_id: str,
        title: str = None,
        description: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
        deadline: datetime = None,
    ) -> Hatm:
        return self._hatm_repository.update(
            hatm_id, title, description, is_public, is_completed, is_published, deadline
        )

    def delete_hatm(self, hatm_id: str) -> None:
        self._hatm_repository.delete(hatm_id)


class JuzService:
    def __init__(self, juz_repository: AbstractJuzRepository):
        self._juz_repository = juz_repository

    def get_juz(self, juz_id: str) -> Juz:
        return self._juz_repository.get(juz_id)

    def list_juzs(
        self, hatm_id: str = None, user_id: str = None, status: JuzStatus = None
    ) -> list[Juz]:
        return self._juz_repository.list(hatm_id, user_id, status)

    def create_juz(
        self,
        hatm_id: str,
        user_id: str,
        juz_number: int,
        status: JuzStatus,
        deadline: datetime,
    ) -> Juz:
        return self._juz_repository.create(
            hatm_id, user_id, juz_number, status, deadline
        )

    def update_juz(
        self, juz_id: str, status: JuzStatus = None, deadline: datetime = None
    ) -> Juz:
        return self._juz_repository.update(juz_id, status, deadline)

    def delete_juz(self, juz_id: str) -> None:
        self._juz_repository.delete(juz_id)
