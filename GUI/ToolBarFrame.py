import tkinter as tk
from tkinter import ttk
from Tools.AppData import AppData
from PIL import Image, ImageTk


class ToolBarFrame(ttk.Frame):
    def __init__(self, container, app_data: AppData, change_changeable_frame_callback):
        super().__init__(container, height=50)
        self.change_changeable_frame_callback = change_changeable_frame_callback

        boton_abrir = self._create_button(self, 'Abrir', 'Assets/abrir.png')
        boton_abrir.grid(row=0, column=0, sticky='NSEW', padx=5)

        boton_guardar = self._create_button(self, 'Guardar', 'Assets/guardar.png')
        boton_guardar.grid(row=0, column=1, sticky='NSEW', padx=(10, 20))

        boton_pintar = self._create_button(self, 'ROI', 'Assets/editar.png')
        boton_pintar.grid(row=0, column=2, sticky='NSEW', padx=(15, 5))

        boton_3d = self._create_button(self, 'Modelo 3D', 'Assets/3d.png')
        boton_3d.grid(row=0, column=3, sticky='NSEW', padx=0)

        # -- PATIENTS COMBOBOX
        self.grid_columnconfigure(4, weight=1)
        ttk.Label(self, text='Patient:').grid(row=0, column=4, sticky='E')

        self.selected_patient = tk.StringVar(value=0)
        self.series_box = ttk.Combobox(master=self,
                                       textvariable=self.selected_patient,
                                       state='readonly',
                                       width=15)
        self.series_box.grid(row=0, column=5, sticky='E')
        self.series_box['values'] = tuple('  ' + study.patient_name for study in app_data.studies)
        self.series_box.current(0)
        self.series_box.bind('<<ComboboxSelected>>', self.patient_selection)
        # --

        separator = ttk.Separator(self, orient='horizontal', style='Light.TSeparator')
        separator.grid(row=1, column=0, sticky="ew", columnspan=6, pady=(10, 0))

    def patient_selection(self, event):
        self.change_changeable_frame_callback(self.series_box.current())

    @staticmethod
    def _create_button(container, text, icon_path):
        button_frame = ttk.Frame(container, height=150)
        button_frame.grid_columnconfigure(0, weight=1)
        label = ttk.Label(button_frame,
                          text=text,
                          font=('Verdana', 12))
        label.grid(row=1, column=0)

        photo = tk.PhotoImage(file=icon_path)
        boton = tk.Button(button_frame,
                          image=photo)
        boton.config(image=photo)
        boton.image = photo
        boton.grid(row=0, column=0)

        return button_frame
