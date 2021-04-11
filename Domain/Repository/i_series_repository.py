from abc import ABC, abstractmethod
from typing import List
from Domain.Model import ZSeries


class ISeriesRepository:
    @abstractmethod
    def get_all_series(self) -> List[ZSeries]:
        pass

    @abstractmethod
    def get_series_from_pk(self, z_pk) -> ZSeries:
        pass

    @abstractmethod
    def get_series_from_uid(self, z_uid) -> ZSeries:
        pass

    @abstractmethod
    def get_series_from_study_pk(self, z_pk) -> List[ZSeries]:
        pass

