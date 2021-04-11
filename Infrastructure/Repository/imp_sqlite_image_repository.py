from Domain.Repository import IImageRepository, IRoiRepository
from Domain.Model import ZImage
from Infrastructure.Repository import connection_to_db
from typing import List


class ImpSqliteImageRepository(IImageRepository):
    def __init__(self, roi_repository: IRoiRepository):
        self.roi_repository = roi_repository

    def get_all_images(self) -> List[ZImage]:
        pass

    def get_image_from_pk(self, z_pk) -> List[ZImage]:
        pass

    def get_images_from_series_pk(self, z_series_pk) -> List[ZImage]:
        images_list = self._get_images_from_series_pk_with_connection(z_series_pk)
        return images_list

    @connection_to_db
    def _get_images_from_series_pk_with_connection(self, z_series_pk, **kwargs):
        images_list = []
        cursor = kwargs['cursor']
        query = '''SELECT Z_PK, Z_SERIES, Z_SOP_INSTANCE_UID, Z_INSTANCE_NUMBER, Z_PATH, Z_WIDTH, Z_HEIGHT
                   FROM Z_IMAGE
                   WHERE Z_SERIES LIKE ?'''
        cursor.execute(query, (str(z_series_pk),))
        records = cursor.fetchall()

        for row in records:
            image_pk = row[0]
            z_series = row[1]
            z_sop_instance_uid = row[2]
            z_index = int(row[3])
            z_path = row[4]
            z_width = int(row[5])
            z_height = int(row[6])

            rois = self.roi_repository.get_rois_from_image_pk(image_pk)
            new_image = ZImage(image_pk, rois, z_sop_instance_uid, z_index, z_path, z_width, z_height)
            images_list.append(new_image)
        return images_list

    def get_image_from_sop(self, z_sop) -> List[ZImage]:
        pass
