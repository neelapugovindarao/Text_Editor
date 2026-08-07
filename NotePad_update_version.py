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

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File",menu=file_menu)


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


def clear(event=None):
    global current_file
    text_area.delete("1.0", tk.END)
    current_file = None
    root.title("Text Editor")


def on_exit():
    if root.title().startswith("*"):
        ans = messagebox.askyesnocancel("Unsaved Changes", "Save before exiting?")
        if ans is None:
            return
        if ans:
            save()
    root.quit()

# ── Edit Operations ────────────────────────────────────────────────────────────
def cut(event=None):
    if text_area.tag_ranges("sel"):
        text_area.event_generate("<<Cut>>")


def copy(event=None):
    if text_area.tag_ranges("sel"):
        text_area.event_generate("<<Copy>>")


def undo(event=None):
    try:
        text_area.edit_undo()
    except tk.TclError:
        pass          # Nothing left to undo


def redo(event=None):
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass          # Nothing left to redo

def redo(event=None):
    try:
        text_area.edit_redo()
    except tk.TclError:
        pass          # Nothing left to redo

def select_all(event=None):
    text_area.tag_add("sel", "1.0", tk.END)
    return "break"   # Prevent default so it doesn't type 'a'



# ── Find & Replace Window ──────────────────────────────────────────────────────
def find_replace(event=None):
    win = tk.Toplevel(root)
    win.title("Find & Replace")
    win.geometry("370x130")
    win.resizable(False, False)
    win.transient(root)      # Stay on top of main window
    win.grab_set()

    tk.Label(win, text="Find:",    width=8, anchor="e").grid(row=0, column=0, padx=6, pady=8)
    tk.Label(win, text="Replace:", width=8, anchor="e").grid(row=1, column=0, padx=6, pady=4)

    find_var    = tk.StringVar()
    replace_var = tk.StringVar()

    find_entry    = tk.Entry(win, textvariable=find_var,    width=28)
    replace_entry = tk.Entry(win, textvariable=replace_var, width=28)
    find_entry.grid(row=0, column=1, columnspan=2, padx=4)
    replace_entry.grid(row=1, column=1, columnspan=2, padx=4)
    find_entry.focus()

    info_label = tk.Label(win, text="", fg="gray")
    info_label.grid(row=3, column=0, columnspan=3, pady=2)

    def do_find():
        text_area.tag_remove("found", "1.0", tk.END)
        needle = find_var.get()
        if not needle:
            return
        count, start = 0, "1.0"
        while True:
            idx = text_area.search(needle, start, nocase=True, stopindex=tk.END)
            if not idx:
                break
            end = f"{idx}+{len(needle)}c"
            text_area.tag_add("found", idx, end)
            start = end
            count += 1
        text_area.tag_config("found", background="yellow", foreground="black")
        info_label.config(text=f"{count} match(es) found")


    def do_replace_all():
        needle = find_var.get()
        replacement = replace_var.get()
        if not needle:
            return
        content = text_area.get("1.0", tk.END)
        new_content = content.replace(needle, replacement)
        replaced = content.count(needle)
        text_area.delete("1.0", tk.END)
        text_area.insert("1.0", new_content)
        text_area.tag_remove("found", "1.0", tk.END)
        info_label.config(text=f"{replaced} replacement(s) made")


    
    tk.Button(win, text="Find All",   command=do_find,  width=12).grid(row=2, column=0, pady=8, padx=4)
    tk.Button(win, text="Replace All",command=do_replace_all, width=12).grid(row=2, column=1, pady=8, padx=4)
    tk.Button(win, text="Close",  command=win.destroy,width=8 ).grid(row=2, column=2, pady=8, padx=4)


root.bind("<Control-o>", open_file)
root.bind("<Control-s>", save)
root.bind("<Control-S>", save_as)      # Ctrl+Shift+S
root.bind("<Control-z>", undo)
root.bind("<Control-y>", redo)
root.bind("<Control-a>", select_all)
root.bind("<Control-h>", find_replace)


root.mainloop()

