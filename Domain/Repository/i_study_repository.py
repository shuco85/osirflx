from abc import ABC, abstractmethod
from typing import List
from Domain.Model import ZStudy


class IStudyRepository:
    @abstractmethod
    def get_all_studies(self) -> List[ZStudy]:
        pass

    @abstractmethod
    def get_study_from_pk(self) -> ZStudy:
        pass

    @abstractmethod
    def get_study_from_uid(self) -> ZStudy:
        pass
