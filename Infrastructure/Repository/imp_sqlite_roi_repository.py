from Domain.Repository import IRoiRepository
from Domain.Model import ZRoi
from Infrastructure.Repository import connection_to_db
from typing import List
import ast


class ImpSqliteRoiRepository(IRoiRepository):
    def __init__(self):
        pass

    def get_all_rois(self) -> List[ZRoi]:
        pass

    def get_image_from_pk(self, z_pk) -> ZRoi:
        pass

    def get_rois_from_image_pk(self, z_image_pk) -> List[ZRoi]:
        rois_list = self._get_rois_from_image_pk_with_connection(z_image_pk)
        return rois_list

    @connection_to_db
    def _get_rois_from_image_pk_with_connection(self, z_image_pk, **kwargs):
        rois_list = []
        cursor = kwargs['cursor']
        query = '''SELECT Z_PK, Z_IMAGE, Z_INDEX, Z_ROI_TYPE, Z_POINTS_PX
                   FROM Z_ROI
                   WHERE Z_IMAGE LIKE ?'''
        cursor.execute(query, (str(z_image_pk),))
        records = cursor.fetchall()
        for row in records:
            roi_pk = row[0]
            z_image_fk = row[1]
            z_index = row[2]
            z_roi_type = row[3]
            z_points_px = ast.literal_eval(row[4])
            new_roi = ZRoi(roi_pk, roi_type=z_roi_type, index=z_index, points_px=z_points_px)
            rois_list.append(new_roi)
        return rois_list
