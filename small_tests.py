import tkinter as tk
import ttkthemes
from ttkthemes import ThemedStyle

root = tk.Tk()
style = ThemedStyle(root)
print(style.theme_names())
root.destroy()