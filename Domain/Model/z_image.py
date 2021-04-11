from pydicom import dcmread
from pydicom.pixel_data_handlers.util import apply_voi_lut, apply_modality_lut
from typing import List
import numpy as np
from PIL import Image, ImageDraw


class ZImage:
    def __init__(self, pk, rois, sop_instance_uid, index, path, width, height):
        self.pk = pk
        self.sop_instance_uid = sop_instance_uid
        self.index = index
        self.path = path
        self.width = width
        self.height = height
        self.rois = rois
        self._index_generator = 0

    def __str__(self):
        rois_string = ""
        for index, roi in enumerate(self.rois):
            rois_string += str(roi)
        return(f"Primary Key Image: {self.pk}\n" +
               f"Sop Instance UID: {self.sop_instance_uid}\n" +
               f"Index: {self.index}\n" +
               f"Path: {self.path}\n" +
               f"Width: {self.width}\n" +
               f"height: {self.height}\n" +
               f"Number of rois: {str(len(self.rois))}\n" +
               '------------------------------\n' +
               f"ROIS: \n{rois_string}\n")

    def __len__(self):
        return len(self.rois)

    def __getitem__(self, item):
        if isinstance(item, str):
            for roi in self.rois:
                if roi.pk == int(item):
                    return roi

        else:
            return self.rois[item]
        return None

    def __iter__(self):
        return self

    def __next__(self):
        self._index_generator += 1

        try:
            return self.rois[self._index_generator - 1]
        except IndexError:
            self._index_generator = 0
            raise StopIteration

    def append_roi(self, roi):
        self.rois.append(roi)

    def get_visual_pixel_array(self):
        """
        Esta funcion convierte las intensidades de los valores @dicom_img adaptándolos a
        una mejor visión humana

        Parametros
        ----------
        dicom_img: a DICOM image

        Devuelve
        --------
        img_255: el array de entrada, aplicando unos cambios en los valores de intensidades
                 y transformado a uint8
        """

        dicom_img = dcmread(self.path)

        # Aplicamos modificaciones en las intensidades de los píxeles
        img_modality_lut = apply_modality_lut(dicom_img.pixel_array, dicom_img)
        img_voi_lut = apply_voi_lut(img_modality_lut, dicom_img)

        # Convertimos el array de int16 a uint8
        img_uint = img_voi_lut + np.min(img_voi_lut) * -1
        img_255 = (img_uint / (np.max(img_uint) / 255)).astype('uint8')

        return img_255

    def get_image_with_roi(self):
        img_base = Image.fromarray(self.get_visual_pixel_array())
        img_color = Image.new('RGB', (self.width, self.height), 0)
        img_color.paste(img_base)

        for roi in self.rois:
            x_interp, y_interp = roi.get_interpolated_points()
            ImageDraw.Draw(img_color).polygon(tuple((x_interp[i], y_interp[i]) for i in range(0, len(x_interp))),
                                              fill=None, outline="red")

        return img_color

    def get_image(self):
        img_base = Image.fromarray(self.get_visual_pixel_array())
        img_color = Image.new('RGB', (self.width, self.height), 0)
        img_color.paste(img_base)

        return img_color

    def add_roi(self, roi):
        self.rois.append(roi)

''' def __str__(self):
    return f"""sop_instance_uid: \t{self.series.sop_instance_uid}
series_instance_uid: \t{self.series_instance_uid}
study_instance_uid: \t{self.study_instance_uid}"""'''