from Infrastructure.Repository import ImpSqliteStudyRepository, ImpSqliteSeriesRepository, \
    ImpSqliteImageRepository, ImpSqliteRoiRepository, ImpSqliteRoiSeriesRepository


class AppData:
    def __init__(self):
        self.current_patient_index = 0
        self.root = None

        self.roi_repository = ImpSqliteRoiRepository()
        self.roi_series_repository = ImpSqliteRoiSeriesRepository()
        self.image_repository = ImpSqliteImageRepository(self.roi_repository)
        self.series_repository = ImpSqliteSeriesRepository(self.image_repository, self.roi_series_repository)
        self.study_repository = ImpSqliteStudyRepository(self.series_repository)
        self.studies = self.study_repository.get_all_studies()

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
