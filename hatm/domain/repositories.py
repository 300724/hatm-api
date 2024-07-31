from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from hatm.domain.models import Hatm, Juz, JuzStatus


class AbstractHatmRepository(ABC):
    @abstractmethod
    def get(self, hatm_id: str) -> Hatm:
        """
        Get a Hatm object by its ID.
        """

    @abstractmethod
    def list(
        self,
        creator_id: str = None,
        is_public: bool = None,
        is_completed: bool = None,
        is_published: bool = None,
    ) -> List[Hatm]:
        """
        List Hatm objects based on the provided filters.
        """

    @abstractmethod
    def create(
        self,
        creator_id: str,
        title: str,
        description: str,
        is_public: bool,
        deadline: datetime,
    ) -> Hatm:
        """
        Create a new Hatm object.
        """

    @abstractmethod
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
        """
        Update an existing Hatm object.
        """

    @abstractmethod
    def delete(self, hatm_id: str) -> None:
        """
        Delete an existing Hatm object.
        """


class AbstractJuzRepository(ABC):
    @abstractmethod
    def get(self, juz_id: str) -> Juz:
        """
        Get a Juz object by its ID.
        """

    @abstractmethod
    def list(
        self, hatm_id: str = None, user_id: str = None, status: JuzStatus = None
    ) -> List[Juz]:
        """
        List Juz objects based on the provided filters.
        """

    @abstractmethod
    def create(
        self,
        hatm_id: str,
        user_id: str,
        juz_number: int,
        status: JuzStatus,
        deadline: datetime,
    ) -> Juz:
        """
        Create a new Juz object.
        """

    @abstractmethod
    def update(
        self, juz_id: str, status: JuzStatus = None, deadline: datetime = None
    ) -> Juz:
        """
        Update an existing Juz object.
        """

    @abstractmethod
    def delete(self, juz_id: str) -> None:
        """
        Delete an existing Juz object.
        """
