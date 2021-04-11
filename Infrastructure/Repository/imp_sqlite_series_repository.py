from Domain.Repository import ISeriesRepository, IImageRepository, IRoiSeriesRepository
from Domain.Model import ZStudy, ZSeries
from Infrastructure.Repository import connection_to_db
from typing import List


class ImpSqliteSeriesRepository(ISeriesRepository):
    def __init__(self, image_repository: IImageRepository, roi_series_repository: IRoiSeriesRepository):
        self.image_repository = image_repository
        self.roi_series_repository = roi_series_repository

    def get_all_series(self) -> List[ZStudy]:
        pass

    def get_series_from_study_pk(self, z_pk) -> List[ZSeries]:
        series_list = self._get_series_from_pk_with_connection(z_pk)
        return series_list

    @connection_to_db
    def _get_series_from_pk_with_connection(self, z_pk, **kwargs) -> List[ZSeries]:
        series_list = []
        cursor = kwargs['cursor']
        query = '''SELECT Z_PK, Z_STUDY, Z_SERIES_INSTANCE_UID 
                   FROM Z_SERIES
                   WHERE Z_PK LIKE ?'''
        cursor.execute(query, (str(z_pk),))
        records = cursor.fetchall()

        for row in records:
            series_pk = int(row[0])
            study_fk = int(row[1])
            series_instance_uid = row[2]
            images = self.image_repository.get_images_from_series_pk(series_pk)
            roi_series_list = self.roi_series_repository.get_roi_series_from_series_pk(series_pk)
            new_series = ZSeries(series_pk, images, series_instance_uid, roi_series_list)

            series_list.append(new_series)

        return series_list

    def get_series_from_pk(self, z_pk) -> List[ZSeries]:
        pass

    def get_series_from_uid(self, z_uid) -> ZSeries:
        pass
