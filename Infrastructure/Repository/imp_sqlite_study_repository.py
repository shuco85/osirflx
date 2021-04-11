from Domain.Repository import IStudyRepository, ISeriesRepository
from Domain.Model import ZStudy, ZSeries, ZImage, ZRoi, ZRoiSeries
from typing import List
from Infrastructure.Repository import connection_to_db
import sqlite3


class ImpSqliteStudyRepository(IStudyRepository):
    def __init__(self, series_repository: ISeriesRepository):
        self.series_repository = series_repository
        pass

    def get_all_studies(self) -> List[ZStudy]:
        studies_list = self._get_all_studies_with_connection()
        return studies_list

    @connection_to_db
    def _get_all_studies_with_connection(self, **kwargs):
        studies_list = []
        cursor = kwargs['cursor']
        sqlite_select_query = '''SELECT Z_PK, Z_STUDY_INSTANCE_UID, Z_PATIENT_NAME, Z_PATIENT_ID FROM Z_STUDY LIMIT 2   '''
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for row in records:
            study_pk = int(row[0])
            study_instance_uid = row[1]
            patient_name = row[2]
            patient_id = row[3]
            series = self.series_repository.get_series_from_study_pk(study_pk)
            new_study = ZStudy(study_pk, series, study_instance_uid, patient_name, patient_id)
            studies_list.append(new_study)
        return studies_list
