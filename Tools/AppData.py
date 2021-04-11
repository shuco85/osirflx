from Infrastructure.Repository import ImpSqliteStudyRepository, ImpSqliteSeriesRepository, \
    ImpSqliteImageRepository, ImpSqliteRoiRepository


class AppData:
    def __init__(self):
        self.current_patient_index = 0
        self.root = None

        roi_repository = ImpSqliteRoiRepository()
        image_repository = ImpSqliteImageRepository(roi_repository)
        series_repository = ImpSqliteSeriesRepository(image_repository)
        study_repository = ImpSqliteStudyRepository(series_repository)
        self.studies = study_repository.get_all_studies()

    def set_root(self, root):
        self.root = root

    def change_current_series(self, index):
        if index != self.current_patient_index:
            self.current_patient_index = index
            self.update_bindings()

    def update_bindings(self):
        main_frame = self.root.main_frame
        current_changeable_frame = main_frame.changeable_frames[self.current_patient_index]
        callback = current_changeable_frame.thumbnails_frame.change_main_photo_and_style_and_scroll

        self.root.bind('<Left>', lambda e: callback(0, e))
        self.root.bind('<Right>', lambda e: callback(0, e))
