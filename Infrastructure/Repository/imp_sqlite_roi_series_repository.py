from Domain.Repository import IRoiSeriesRepository
from Domain.Model import ZRoiSeries
from Infrastructure.Repository import connection_to_db
from typing import List


class ImpSqliteRoiSeriesRepository(IRoiSeriesRepository):

    def get_all_roi_series(self) -> List[ZRoiSeries]:
        pass

    def get_roi_series_from_pk(self, z_pk) -> ZRoiSeries:
        pass

    def get_roi_series_from_series_pk(self, z_series_pk) -> List[ZRoiSeries]:
        return self._get_roi_series_from_series_pk_with_connection(z_series_pk)

    @connection_to_db
    def _get_roi_series_from_series_pk_with_connection(self, z_series_pk, **kwargs) -> List[ZRoiSeries]:
        roi_series_list = []
        cursor = kwargs['cursor']
        query = '''SELECT Z_PK, Z_SERIES, Z_NAME, Z_COLOR
                   FROM Z_ROI_SERIES
                   WHERE Z_SERIES LIKE ?'''
        cursor.execute(query, (str(z_series_pk),))
        records = cursor.fetchall()

        for row in records:
            roi_series_pk = int(row[0])
            z_series_fk = int(row[1])
            z_name = row[2]
            z_color = row[3]
            new_row_series = ZRoiSeries(roi_series_pk, z_name, z_color)
            roi_series_list.append(new_row_series)

        return roi_series_list

    def add_new_roi_series_in_series(self, z_series_pk, z_name, z_color) -> ZRoiSeries:
        return self._add_new_roi_series_in_series_with_connection(z_series_pk, z_name, z_color)

    @connection_to_db
    def _add_new_roi_series_in_series_with_connection(self, z_series_pk, z_name, z_color, **kwargs) -> ZRoiSeries:
        cursor = kwargs['cursor']
        sql = ''' INSERT INTO Z_ROI_SERIES (Z_SERIES, Z_NAME, Z_COLOR)
                  VALUES(?,?,?) '''
        cursor.execute(sql, (str(z_series_pk), str(z_name), str(z_color),))
        roi_series_pk = cursor.lastrowid
        new_roi_series = ZRoiSeries(roi_series_pk, z_name, z_color)
        return new_roi_series
