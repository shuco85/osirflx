class ZSeries:
    def __init__(self, pk, images, series_instance_uid, roi_series_list):
        self.pk = pk
        self.images = images
        self.series_instance_uid = series_instance_uid
        self.images = images
        self.roi_series_list = roi_series_list
        self._index_generator = 0

    def __str__(self):
        return(f"Primary Key Series: {self.pk}\n" +
               f"Series Instance UID: {self.series_instance_uid}\n" +
               f"Images Lenght: {len(self)}\n")

    def __len__(self):
        return len(self.images)

    def __getitem__(self, item):
        return self.images[item]

    def __iter__(self):
        return self

    def __next__(self):
        self._index_generator += 1

        try:
            return self.images[self._index_generator - 1]
        except IndexError:
            self._index_generator = 0
            raise StopIteration

    def get_roi_series_from_name(self, name):
        for roi_series in self.roi_series_list:
            if roi_series.name == name:
                return roi_series