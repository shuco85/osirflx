class ZStudy:
    def __init__(self, pk, series, study_instance_uid, patient_name, patient_id):
        self.pk = pk
        self.series = series
        self.study_instance_uid = study_instance_uid
        self.patient_name = patient_name
        self.patient_id = patient_id

    def __str__(self):
        series_string = ''
        for serie in self.series:
            series_string += str(serie)
        return(f"Primary Key Study: {self.pk}\n" +
               f"Study Instance UID: {self.study_instance_uid}\n" +
               f"Patient Name: {self.patient_name}\n" +
               f"Patient ID: {self.patient_id}\n" +
               'Series: ----\n' +
               series_string)