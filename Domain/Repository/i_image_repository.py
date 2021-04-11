from abc import ABC, abstractmethod
from typing import List
from Domain.Model import ZImage


class IImageRepository:
    @abstractmethod
    def get_all_images(self) -> List[ZImage]:
        pass

    @abstractmethod
    def get_image_from_pk(self, z_pk) -> List[ZImage]:
        pass

    @abstractmethod
    def get_images_from_series_pk(self, z_series_pk) -> List[ZImage]:
        pass

    @abstractmethod
    def get_image_from_sop(self, z_sop) -> List[ZImage]:
        pass
