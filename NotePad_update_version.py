import tkinter as tk
from tkinter import filedialog , messagebox


root = tk.Tk()
root.title("Text Editor")
root.geometry("650x500")

#Text area + scorllbar
frame = tk.Frame(root)

frame.pack(expand = True , fill = "both")

scrollbar = tk.Scrollbar(frame)

scrollbar.pack(side = "right" , fill = "y")


root.mainloop()

