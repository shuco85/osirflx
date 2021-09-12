from GUI.Osirflx import Osirflx
from Tools.AppData import AppData
import tkinter as tk

app_data = AppData()

root = Osirflx(app_data)
app_data.set_root(root)
app_data.update_bindings()
app_data.func_tirar()

# Application Icon
img = tk.Image("photo", file="Assets/icon.png")
root.tk.call('wm', 'iconphoto', root._w, img)


root.mainloop()
