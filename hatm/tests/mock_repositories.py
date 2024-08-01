from datetime import datetime

from hatm.domain.models import Hatm, Juz, JuzStatus
from hatm.domain.repositories import (AbstractHatmRepository,
                                      AbstractJuzRepository)


class MockHatmRepository(AbstractHatmRepository):
    _repository = None  # todo: poka bilmeim, ozin koresin go

    def get(self, hatm_id: str) -> Hatm:
        pass

    def list(
        self,
        creator_id: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
    ) -> list[Hatm]:
        pass

    def create(
        self,
        creator_id: str,
        title: str,
        description: str,
        is_public: bool,
        deadline: datetime,
    ) -> Hatm:
        pass

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
        pass

    def delete(self, hatm_id: str) -> None:
        pass


class MockJuzRepository(AbstractJuzRepository):
    _repository = None  # todo: poka bilmeim, ozin koresin go

    def get(self, juz_id: str) -> Juz:
        pass

    def list(
        self, hatm_id: str = None, user_id: str = None, status: JuzStatus = None
    ) -> list[Juz]:
        pass

    def create(
        self,
        hatm_id: str,
        user_id: str,
        juz_number: int,
        status: JuzStatus,
        deadline: datetime,
    ) -> Juz:
        pass

    def update(
        self, juz_id: str, status: JuzStatus = None, deadline: datetime = None
    ) -> Juz:
        pass

    def delete(self, juz_id: str) -> None:
        pass
