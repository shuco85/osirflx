from abc import ABC, abstractmethod
from typing import List
from Domain.Model import ZRoiSeries


class IRoiSeriesRepository:
    @abstractmethod
    def get_all_roi_series(self) -> List[ZRoiSeries]:
        pass

    @abstractmethod
    def get_roi_series_from_pk(self, z_pk) -> ZRoiSeries:
        pass

    @abstractmethod
    def add_new_roi_series_in_series(self, z_series_pk, z_name, z_color) -> ZRoiSeries:
        pass

    @abstractmethod
    def get_roi_series_from_series_pk(self, z_series_pk) -> List[ZRoiSeries]:
        pass
