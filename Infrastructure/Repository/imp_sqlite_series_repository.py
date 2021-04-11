from Domain.Repository import ISeriesRepository, IImageRepository
from Domain.Model import ZStudy, ZSeries
from Infrastructure.Repository import connection_to_db
from typing import List


class ImpSqliteSeriesRepository(ISeriesRepository):
    def __init__(self, image_repository: IImageRepository):
        self.image_repository = image_repository

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
            series_pk = row[0]
            study_fk = row[1]
            series_instance_uid = row[2]
            images = self.image_repository.get_images_from_series_pk(series_pk)
            new_series = ZSeries(series_pk, images, series_instance_uid)

            series_list.append(new_series)

        return series_list

    def get_series_from_pk(self, z_pk) -> List[ZSeries]:
        pass

    def get_series_from_uid(self, z_uid) -> ZSeries:
        pass
