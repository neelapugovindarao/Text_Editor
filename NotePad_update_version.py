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

text_area = tk.Text(frame , wrap = "word" , font = ("consolas" , 15) , 
                    undo = True , maxundo = 50 , yscrollcommand = scrollbar.set)
text_area.pack(expand = True , fill = "both")

scrollbar.configure(command = text_area.yview)




root.mainloop()

