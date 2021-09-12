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
            roi_pk = int(row[0])
            z_image_fk = int(row[1])
            z_index = int(row[2])
            z_roi_type = int(row[3]) if row[3] else None
            z_points_px = ast.literal_eval(row[4])
            new_roi = ZRoi(roi_pk, roi_series=z_roi_type, index=z_index, points_px=z_points_px)
            rois_list.append(new_roi)
        return rois_list

    def delete_roi_from_pk(self, z_pk) -> None:
        self._delete_roi_from_pk(z_pk)

    @connection_to_db
    def _delete_roi_from_pk(self, z_pk, **kwargs) -> None:
        cursor = kwargs['cursor']
        query = '''DELETE
                   FROM Z_ROI
                   WHERE Z_PK LIKE ?'''
        cursor.execute(query, (z_pk, ))

    def update_roi(self, z_roi) -> None:
        self._update_roi_with_connection(z_roi)

    @connection_to_db
    def _update_roi_with_connection(self, z_roi, **kwargs) -> None:
        cursor = kwargs['cursor']
        query = '''UPDATE Z_ROI
                   SET Z_ROI_TYPE = ?, Z_POINTS_PX = ?
                   WHERE Z_PK LIKE ?'''
        cursor.execute(query, (str(z_roi.roi_series), str(z_roi.points_px), str(z_roi.pk),))
