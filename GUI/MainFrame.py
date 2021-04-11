import tkinter as tk
from tkinter import ttk
from GUI.ChangeableFrame import ChangeableFrame
from GUI.ToolBarFrame import ToolBarFrame
from Tools.AppData import AppData


class MainFrame(ttk.Frame):
    def __init__(self, container, app_data: AppData, **kwargs):
        super().__init__(container, style='Main.TFrame', **kwargs)
        self.app_data = app_data

        # MAINFRAME CONFIGURATION
        self.grid_columnconfigure(0, weight=1)

        # -- TOOLBAR FRAME
        self.toolbar_frame = ToolBarFrame(self,
                                          self.app_data,
                                          self.change_changeable_frame)
        self.toolbar_frame.grid(row=0, column=0, sticky='EW', padx=10, pady=15)
        # --

        # -- CHANGEABLE FRAME
        self.changeable_frames = []
        for study in self.app_data.studies:
            self.changeable_frames.append(ChangeableFrame(self, self.app_data, study))
        self.changeable_frames[0].grid(row=2, column=0, sticky='NSEW')
        # --

    def change_changeable_frame(self, index):
        self.changeable_frames[self.app_data.current_patient_index].grid_forget()
        self.app_data.change_current_series(index)
        self.changeable_frames[self.app_data.current_patient_index].grid(row=1, column=0, sticky='NSEW')
