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

# ── Status Bar 

status_bar = tk.Label(root , text ="Ln 1 , col 1",padx =10,anchor = "e" , relief= "sunken",
                      font=("Consolas", 10))

status_bar.pack(side = "bottom" , fill = "x")

def update_status(event=None):
    pos = text_area.index(tk.INSERT)
    line, col = pos.split(".")
    status_bar.config(text=f"Ln {line}, Col {int(col)+1}")


text_area.bind("<KeyRelease>", update_status)
text_area.bind("<ButtonRelease>", update_status)


def mark_modified(event=None):
    if not root.title().startswith("*"):
        root.title("*" + root.title())


def update_title(path):
    root.title(path.split("/")[-1] + " — Text Editor")

text_area.bind("<<Modified>>", mark_modified)

# ── File Operations ────────────────────────────────────────────────────────────
def open_file(event=None):
    global current_file
    path = filedialog.askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
      if path:
        with open(path, "r") as f:
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, f.read())
        current_file = path
        update_title(path)
        text_area.edit_reset()    # Clear undo history after fresh open

def save(event=None):
    global current_file
    path = current_file or filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]

      if path:
        try:
            with open(path, "w") as f:
                f.write(text_area.get("1.0", tk.END).rstrip())
            current_file = path
            update_title(path)
          
        except Exception as e:
            messagebox.showerror("Error", f"Could not save:\n{e}")


def save_as(event=None):
    global current_file
    current_file = None
    save()






root.mainloop()

