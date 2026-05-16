import tkinter as tk
from tkinter import filedialog # lib for from tkinter

root = tk.Tk()
root.title("Text_Editor_1")
root.geometry("450x350")
text_area = tk.Text(root , wrap = "word" , font = ("" , 25))
text_area.pack(expand = True , fill = "both") # to increse the size of the editio as increse the screen

def open_file():
    path = filedialog.askopenfilename(filetype = [("TEXT file" , "*txt")])
    if path:
        with open(path , "r") as file:
            text_area.delete("1.0" , tk.END)
            text_area.insert(tk.END , file.read())
            
def save():
    path = filedialog.asksaveasfilename(defaultextension = ".txt")
    if path:
        try:
            with open(path , "w") as file:
                text = text_area.get("1.0" , tk.END).rstrip()
                file.write(text)
        except Exception as e:
            print("Error : " ,e)


def clear():
    text_area.delete("1.0" , tk.END)
    
menu = tk.Menu(root)
root.config(menu=menu)                     # this thre lines playe a major role 
file_menu = tk.Menu(menu , tearoff = 0)    # Creates the top-level menu bar and attaches it to the main window
menu.add_cascade(label = "File" , menu = file_menu)



file_menu.add_command(label = "Open" , command = open_file)
file_menu.add_command(label = "save" , command = save)
file_menu.add_command(label = "Clear" , command = clear)
file_menu.add_command(label = "Exit" , command = root.quit)    
    

root.mainloop()
