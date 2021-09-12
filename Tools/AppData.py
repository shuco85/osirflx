from Infrastructure.Repository import ImpSqliteStudyRepository, ImpSqliteSeriesRepository, \
    ImpSqliteImageRepository, ImpSqliteRoiRepository, ImpSqliteRoiSeriesRepository

import PIL
import cv2
import os
from tensorflow.python.client import device_lib
from fastai.basics import *
from fastai.vision import models
from fastai.vision.all import *
from fastai.metrics import *
from fastai.data.all import *
from fastai.callback import *
from pathlib import Path
import random
from tensorflow.python.client import device_lib
import torchvision.transforms as transforms

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

        self.tirar = False

    def func_tirar(self):
        aux = device_lib.list_local_devices()
        print('----------------')
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model = torch.jit.load("Assets/unet.pth")
        model = model.cpu()
        model.eval()
        import torchvision.transforms as transforms

        def transform_image(image):
            my_transforms = transforms.Compose([transforms.ToTensor(),
                                                transforms.Normalize(
                                                    [0.485, 0.456, 0.406],
                                                    [0.229, 0.224, 0.225])])
            image_aux = image
            return my_transforms(image_aux).unsqueeze(0).to(device)

        img = PIL.Image.open('Assets/dataset/Images/test/orig-' + '4795' + '.png')
        img = img.convert('RGB')
        image = transforms.Resize((512, 512))(img)
        tensor = transform_image(image=image)
        model.to(device)
        with torch.no_grad():
            outputs = model(tensor)
        outputs = torch.argmax(outputs, 1)

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

    def predict_rois(self):
        main_frame = self.root.main_frame
        current_changeable_frame = main_frame.changeable_frames[self.current_patient_index]
        index = current_changeable_frame.current_canvas_and_data_index
        current_changeable_frame.canvas_and_frames[index].canvas.predict_roi_callback()


