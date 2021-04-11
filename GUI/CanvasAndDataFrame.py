import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Domain.Model import ZImage
from GUI.ThumbnailsFrame import ThumbnailsFrame
import numpy as np
from Domain.Model import ZStudy, ZImage
from Tools.AppData import AppData
from scipy.interpolate import splprep, splev

ROI_POINT_RADIUS = 3


class CanvasAndDataFrame(ttk.Frame):
    def __init__(self, container, app_data, study, image):
        super().__init__(container)

        self.app_data = app_data

        # -- DATA FRAME
        self.study = study
        self.image = image
        self.grid_rowconfigure(0, weight=1)
        self.image_data_frame = DataFrame(self, study, image, study.patient_name)
        self.image_data_frame.grid(row=0, column=1, sticky='NSEW', padx=10, pady=5)
        # --

        # -- CANVAS
        self.canvas = MyCanvas(self, app_data, study, image)
        self.canvas.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)
        # --

        '''# -- COORDINATES
        self.coordinates = tk.StringVar(value='0 x 0')
        self.label_coordinates = ttk.Label(self,
                                           textvariable=self.coordinates,
                                           style='Coordinates.TLabel')
        self.label_coordinates.grid(row=0, column=0, sticky='NW', padx=5, pady=5)
        self.canvas_frame = ttk.Frame(self)
        self.canvas_frame.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)
        self.label_main_photo = tk.Canvas(self.canvas_frame,
                                          borderwidth=0,
                                          width=512,
                                          height=512,
                                          bd=-3,
                                          bg='black')
        self.label_main_photo.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)
        photo = image.get_image_with_roi()
        self.photo_flx = ImageTk.PhotoImage(photo)
        self.label_main_photo.create_image(0, 0, image=self.photo_flx, anchor='nw')
        # ---- LABEL_COORDINATES
        self.coordinates = tk.StringVar(value='0 x 0')
        self.label_coordinates = ttk.Label(self.canvas_frame,
                                           textvariable=self.coordinates,
                                           style='Coordinates.TLabel')
        self.label_coordinates.grid(row=0, column=0, sticky='NW', padx=5, pady=5)
        # --

        # ---- EVENTS
        self.label_main_photo.bind('<Motion>', self.update_coordinates)
        self.label_main_photo.bind('<B1-Motion>', self.paint)
        # --

    def paint(self, e):
        x1 = e.x - 1
        y1 = e.y - 1
        x2 = e.x + 1
        y2 = e.y + 1
        self.label_main_photo.create_line(x1, y1, x2, y2, fill='green', smooth=True)

    def update_coordinates(self, event):
        self.coordinates.set('{} x {}'.format(max(0, event.x), max(0, event.y)))'''

        # self.canvas.bind('<Motion>', self.update_coordinates)

    def update_coordinates(self, event):
        self.coordinates.set('{} x {}'.format(max(0, event.x), max(0, event.y)))


class DataFrame(ttk.Frame):
    def __init__(self, container, study: ZStudy, image_data: ZImage, patient_name):
        super().__init__(container)
        self.grid_columnconfigure(0, weight=1)
        self.study = study
        self.image_data = image_data

        self.sop_number = tk.StringVar()
        ttk.Label(self, text='Sop Number: ').grid(row=1, column=0, sticky='W')
        ttk.Label(self, textvariable=self.sop_number).grid(row=1, column=1, sticky='W')
        self.series_instance_uid = tk.StringVar()
        ttk.Label(self, text='Series Instance UID: ').grid(row=2, column=0, sticky='W')
        ttk.Label(self, textvariable=self.series_instance_uid).grid(row=2, column=1, sticky='W')
        self.study_instance_uid = tk.StringVar()
        ttk.Label(self, text='Study Instance UID: ').grid(row=3, column=0, sticky='W')
        ttk.Label(self, textvariable=self.study_instance_uid).grid(row=3, column=1, sticky='W')
        self.number_rois = tk.StringVar()
        ttk.Label(self, text='Number of ROIs: ').grid(row=4, column=0, sticky='W')
        ttk.Label(self, textvariable=self.number_rois).grid(row=4, column=1, sticky='W')
        self.file_path = tk.StringVar()
        ttk.Label(self, text='File Path: ').grid(row=5, column=0, sticky='W')
        ttk.Label(self, textvariable=self.file_path).grid(row=5, column=1, sticky='W')
        self.image_height = tk.StringVar()
        ttk.Label(self, text='Height: ').grid(row=6, column=0, sticky='W')
        ttk.Label(self, textvariable=self.image_height).grid(row=6, column=1, sticky='W')
        self.image_width = tk.StringVar()
        ttk.Label(self, text='Width: ').grid(row=7, column=0, sticky='W')
        ttk.Label(self, textvariable=self.image_width).grid(row=7, column=1, sticky='W')

        for element in self.winfo_children():
            if element['text']:
                element['style'] = 'Bold.DataImage.TLabel'
            else:
                element['style'] = 'DataImage.TLabel'

        title_label = ttk.Label(self, text='Paciente ' + patient_name)
        title_label.grid(row=0, column=0, columnspan=2, sticky='EW', pady=20)
        title_label.configure(style='Title.DataImage.TLabel')

        self.update_values()

    def update_image_data(self, image_data):
        self.image_data = image_data
        self.update_values()

    def update_values(self):
        self.sop_number.set(self.image_data.sop_instance_uid[-20:])
        self.study_instance_uid.set(self.study.study_instance_uid[-20:])
        self.series_instance_uid.set(self.study.series[0].series_instance_uid[-20:])
        self.number_rois.set(str(len(self.image_data.rois)))
        self.file_path.set(self.image_data.path)
        self.image_height.set(self.image_data.height)
        self.image_width.set(self.image_data.width)


# ------------------------------------------------------------------------


# -------------------------------- CANVAS --------------------------------
class MyCanvas(tk.Canvas):
    def __init__(self, container, app_data, study, image: ZImage):
        self.canvas_width = image.width
        self.canvas_height = image.height

        self.rois = image.rois
        self.rois_drawn = {}

        self.current_point = None
        self.current_drawing_roi = []
        self.dragging = False
        self.current_color = 'yellow'

        super().__init__(container,
                         width=self.canvas_width,
                         height=self.canvas_height,
                         bd=-3,
                         bg='black')

        # -- BACKGROUND
        image_photo = ImageTk.PhotoImage(image.get_image())
        self.create_image(0, 0, image=image_photo, anchor='nw')
        self.image = image_photo
        # --

        # -- EVENTS
        # self.bind('<B1-Motion>', self._move)
        # self.bind('<ButtonPress-1>', self._create_circle_by_event)
        # self.bind('<ButtonRelease-1>', self.stop_move)
        # self.bind('<Double-Button-1>', self._end_roi_by_event)
        # self.bind('<Button-1>', self._create_circle_by_event)
        # self.bind('<Button-2>', self._delete_circle_by_event)
        self.bind("<Motion>", self.check_hand)
        # self.bind("<<ROI_Color_Changed>>", self._print_roi_from_points_interpolated())
        # --
        self.initial_setup()

    def initial_setup(self):
        for roi in self.rois:
            self.rois_drawn[roi.pk] = {}
            for point in roi.points_px:
                canvas_index = self.create_circle(*point, ROI_POINT_RADIUS, fill=self.current_color)
                self.rois_drawn[roi.pk][canvas_index] = point
            self._print_roi_from_points_interpolated(roi.pk)

    def update_roi_canvas(self, color):
        self.current_color = color
        self._print_roi_from_points_interpolated()
        for point in self.roi_points:
            self.itemconfigure(point, fill=self.current_color)

    def _move(self, event):
        if self.current_point is not None:
            self.dragging = True
            self.change_circle_position(self.current_point, event.x, event.y)
            self.roi_points[self.current_point] = (event.x, event.y)
            self._print_roi_from_points_interpolated()

            if self.current_point == 9999999:
                self.roi_points[list(self.roi_points.keys())[0]] = self.roi_points[self.current_point]
            elif self.current_point == list(self.roi_points.keys())[0]:
                self.roi_points[9999999] = self.roi_points[self.current_point]

    def stop_move(self, event):
        if self.dragging:
            self.roi_points[self.current_point] = (event.x, event.y)
            self.dragging = False

    def _create_circle_by_event(self, event):
        if self.current_point is None:
            index = self.create_circle(event.x, event.y, ROI_POINT_RADIUS, fill=self.current_color)
            self.roi_points[index] = (event.x, event.y)
            self._print_roi_from_points_interpolated()

    def _print_roi_from_points(self):
        keys_list = list(self.roi_points.keys())
        for line in self.current_drawing_roi:
            self.delete(line)
        self.current_drawing_roi = []
        for index in range(len(keys_list) - 1):
            line = self.create_line(*self.roi_points[keys_list[index]],
                                    *self.roi_points[keys_list[index + 1]],
                                    fill=self.current_color)
            self.current_drawing_roi.append(line)

        print(self.current_drawing_roi)

    def _print_roi_from_points_interpolated(self, roi_pk):
        # points_px = list(self.roi_points.values())
        points_px = self.rois_drawn[roi_pk].values()

        if len(points_px) < 4:
            # self._print_roi_from_points()
            return

        x = [coords[0] for coords in points_px]
        y = [coords[1] for coords in points_px]

        if roi_pk:
            x.append(x[0])
            y.append(y[0])
            tck, u = splprep([x, y], s=0, per=True)
        else:
            tck, u = splprep([x, y], s=0)

        # evaluate the spline fits for 1000 evenly spaced distance values
        xi, yi = splev(np.linspace(0, 1, 1000), tck)

        '''if self.current_drawing_roi:
            pass
            keys_list = list(self.roi_points.keys())
            for line in self.current_drawing_roi:
                self.delete(line)'''
        self.current_drawing_roi = []
        for index in range(len(xi) - 1):
            line = self.create_line(xi[index], yi[index],
                                    xi[index + 1], yi[index + 1],
                                    fill=self.current_color)
            self.current_drawing_roi.append(line)

    def _delete_circle_by_event(self, event):
        if self.current_point is not None:
            self.delete(self.current_point)
            self.roi_points.pop(self.current_point, None)
            self._print_roi_from_points()

    def _end_roi_by_event(self, event):
        if len(self.roi_points) >= 3:
            self.roi_points[9999999] = self.roi_points[list(self.roi_points.keys())[0]]
            self._print_roi_from_points_interpolated()

    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x - r, y - r, x + r, y + r, **kwargs)

    def change_circle_position(self, index, x, y):
        return self.coords(index,
                           x - ROI_POINT_RADIUS,
                           y - ROI_POINT_RADIUS,
                           x + ROI_POINT_RADIUS,
                           y + ROI_POINT_RADIUS)

    def check_hand(self, event):
        self.create_text(5, 5, fill="white", font="Times 20 italic bold",
                         text='{} x {}'.format(max(0, event.x), max(0, event.y)))
        for z_pk in self.rois_drawn.keys():
            for canvas_index, roi_point in self.rois_drawn[z_pk].items():
                if (
                        roi_point[0] - ROI_POINT_RADIUS < event.x < roi_point[0] + ROI_POINT_RADIUS and
                        roi_point[1] - ROI_POINT_RADIUS < event.y < roi_point[1] + ROI_POINT_RADIUS):
                    self.config(cursor="cross")
                    self.current_point = (z_pk, canvas_index)
                    return


        self.config(cursor="")
        self.current_point = None

# ------------------------------------------------------------------------
