import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Domain.Model import ZImage
from GUI.ThumbnailsFrame import ThumbnailsFrame
from Domain.Model import ZStudy, ZImage
from Tools.AppData import AppData
from GUI.CanvasAndDataFrame import CanvasAndDataFrame


class ChangeableFrame(ttk.Frame):
    def __init__(self, container, app_data: AppData, study: ZStudy):
        super().__init__(container)
        self.current_canvas_and_data_index = 0
        self.app_data = app_data
        self.study = study
        self.grid_columnconfigure(0, weight=1)

        # -- CANVAS_AND_DATA FRAME
        self.canvas_and_frames = [CanvasAndDataFrame(self, image, study) for image in self.study.series[0]]
        self.canvas_and_frames[self.current_canvas_and_data_index].grid(row=1, column=0, sticky='NSEW')

        # -- THUMBNAILS FRAME
        self.grid_rowconfigure(1, weight=1)
        self.thumbnails_frame = ThumbnailsFrame(self,
                                                self.study,
                                                self.change_canvas_and_data_frame_callback)
        self.thumbnails_frame.grid(row=0, column=0, sticky='NSEW')
        # --

    def change_canvas_and_data_frame_callback(self, index=0):
        self.canvas_and_frames[self.current_canvas_and_data_index].grid_forget()
        self.current_canvas_and_data_index = index
        self.canvas_and_frames[self.current_canvas_and_data_index].grid(row=1, column=0)




