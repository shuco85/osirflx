from abc import ABC, abstractmethod
from typing import List
from Domain.Model import ZRoi


class IRoiRepository:
    @abstractmethod
    def get_all_rois(self) -> List[ZRoi]:
        pass

    @abstractmethod
    def get_image_from_pk(self, z_pk) -> ZRoi:
        pass

    @abstractmethod
    def get_rois_from_image_pk(self, z_image_pk) -> List[ZRoi]:
        pass

    @abstractmethod
    def delete_roi_from_pk(self, z_pk) -> None:
        pass

    @abstractmethod
    def update_roi(self, z_roi) -> None:
        pass
