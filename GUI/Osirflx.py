import tkinter as tk
from tkinter import ttk
from GUI.MainFrame import MainFrame
from PIL import Image, ImageTk


class Osirflx(tk.Tk):
    def __init__(self, app_data):
        super().__init__()
        # -- INITIALIZE DATA --
        self.app_data = app_data
        self.iconbitmap('icon.ico')
        # --

        # -- STYlES --
        style = ttk.Style(self)
        #style.theme_use('clam')
        style.configure('Main.TFrame', background='red', bg='red')
        style.configure('Thumbnails.TFrame', background='blue')
        style.configure('Thumbnail.TFrame', background='yellow')
        style.configure('Coordinates.TLabel',
                        background='#0c343d',
                        foreground='black',
                        font=('TkDefault', 15),
                        anchor='W')
        style.configure('DataImage.TLabel',
                        foreground='black',
                        font=('TkDefault', 14),
                        sticky='EW',
                        anchor='W',
                        padding=5)
        style.configure('Bold.DataImage.TLabel',
                        font=('TkDefault', 14, 'bold'))
        style.configure('Title.DataImage.TLabel',
                        font=('TkDefault', 20, 'bold'))

        style.configure('Light.TSeparator',
                        background='red')
        # --

        # -- ROOT CONF --
        self.geometry('1100x850')
        self.title('Osirflx')
        # --

        # -- MENU BAR
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar)
        menu_bar.add_cascade(label='Archivo', menu=file_menu)
        file_menu.add_command(label='Abrir...', command=self.fake_command)
        file_menu.add_command(label='Salir', command=self.fake_command)

        #edit_menu = tk.Menu(menu_bar)
        #edit_menu.add_cascade(label='Edicion', menu=edit_menu)
        #edit_menu.add_command(label='Copiar', command=self.fake_command)
        #edit_menu.add_command(label='Cortar', command=self.fake_command)
        #edit_menu.add_command(label='Pegar', command=self.fake_command)
        # --

        # -- MAIN FRAME --
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.main_frame = MainFrame(self, self.app_data)
        self.main_frame.grid(row=0, column=0, sticky='NSEW')

    def fake_command(self):
        print('Fake Command')
