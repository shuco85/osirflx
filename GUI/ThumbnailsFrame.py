import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


class ThumbnailsFrame(ttk.Frame):
    def __init__(self, container, study, change_canvas_and_data_frame_callback, **kwargs):
        super().__init__(container,
                         height=150,
                         style='Thumbnails.TFrame',
                         **kwargs)

        self.change_canvas_and_data_frame_callback = change_canvas_and_data_frame_callback
        self.thumbnail_selected = 0
        self.thumbnails_list = []

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # -- TO CREATE SCROLLBAR --
        self.canvas = tk.Canvas(self, height=140)
        self._scrollable_frame = ttk.Frame(self.canvas)
        self._scrollable_window = self.canvas.create_window((0, 0),
                                                            window=self._scrollable_frame,
                                                            anchor='w')
        self._scrollable_frame.bind('<Configure>', self._configure_scroll_region)
        # --

        # -- THUMBNAILS CONTAINER
        self.thumbnails_container_frame = ttk.Frame(self._scrollable_frame,
                                                    style='Thumbnails.TFrame')
        self.thumbnails_container_frame.grid(row=0, column=0, sticky='NSEW', padx=10)
        self.thumbnails_container_frame.grid_rowconfigure(0, weight=1)

        _patient_name = study.patient_name
        _images = study.series[0].images

        for idx, image in enumerate(_images):
            thumbnail_frame = ThumbnailFrame(self.thumbnails_container_frame,
                                             image,
                                             idx,
                                             self.change_main_photo_and_style_and_scroll)
            thumbnail_frame.grid(row=0,
                                 column=idx,
                                 padx=10,
                                 pady=10)

            self.thumbnails_list.append(thumbnail_frame)
        # --

        # -- SCROLL BAR AND CANVAS CONFIGURATION--
        self.scrollbar = ttk.Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.grid(row=1, column=0, sticky='EW')
        self.canvas.configure(xscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky='NSEW')
        # --
        self.change_main_photo_and_style_and_scroll(0)

    def _configure_scroll_region(self, *args, **kwargs):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def change_main_photo_and_style_and_scroll(self, index, *args):
        new_selected = index
        current_selected = self.thumbnail_selected

        if args:
            if args[0].keysym == 'Right':
                new_selected = min(current_selected+1, len(self.thumbnails_list)-1)
            if args[0].keysym == 'Left':
                new_selected = max(current_selected-1, 0)

        self.thumbnails_list[current_selected].change_label_style()
        self.thumbnail_selected = new_selected
        self.thumbnails_list[new_selected].change_label_style('red')
        self.change_canvas_and_data_frame_callback(new_selected)


class ThumbnailFrame(ttk.Frame):
    def __init__(self, container, image_data, index_from_zero, thumbnail_callback, **kwargs):
        super().__init__(container,
                         height=120,
                         width=100,
                         style='Thumbnail.TFrame',
                         **kwargs)
        self.thumbnail_callback = thumbnail_callback

        # -- GET DATA FROM THE IMAGE VAR
        sop_instance_uid = image_data.sop_instance_uid
        index = image_data.index
        image = image_data.get_image_with_roi()

        # -- CREATE THUMBNAIL
        image_thumbnail = image.copy()
        image_thumbnail.thumbnail((110, 110), Image.ANTIALIAS)
        image_thumbnail_tk = ImageTk.PhotoImage(image_thumbnail)

        # -- IMAGE LABEL
        label_image = ttk.Label(self)
        label_image.grid(row=0, column=0)
        label_image.configure(image=image_thumbnail_tk)
        label_image.image = image_thumbnail_tk

        # -- LABEL WITH INDEX
        self.label_index = ttk.Label(self, text=str(index))
        self.label_index.grid(row=1, column=0)
        self.label_index.configure(anchor='center')

        self.bind('<Button-1>', lambda e: self._change_main_photo(e))
        label_image.bind('<Button-1>', lambda e: self._change_main_photo(e, index_from_zero))
        self.label_index.bind('<Button-1>', lambda e: self._change_main_photo(e, index_from_zero))

    def _change_main_photo(self, event, index_from_zero):
        self.thumbnail_callback(index_from_zero)

    def change_label_style(self, colour='black'):
        self.label_index.configure(foreground=colour)

