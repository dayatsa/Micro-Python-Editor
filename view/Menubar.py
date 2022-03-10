import tkinter as tk
from tkinter import messagebox

class Menubar:
    def __init__(self, parent, root):
        font_specs = ("ubuntu", 11)
 
        menubar = tk.Menu(root, font=font_specs)
        root.config(menu=menubar)
 
        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File",
                                  accelerator="Ctrl+N",
                                  command=parent.button_new_file_clicked)
        file_dropdown.add_command(label="Open File",
                                  accelerator="Ctrl+O",
                                  command=parent.button_open_file_clicked)
        file_dropdown.add_command(label="Save",
                                  accelerator="Ctrl+S",
                                  command=parent.button_save_clicked)
        file_dropdown.add_command(label="Save As",
                                  accelerator="Ctrl+Shift+S",
                                  command=parent.button_save_as_clicked)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                  command=root.destroy)
 
        run_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        run_dropdown.add_command(label="Run Code",
                                accelerator="Ctrl+R",
                                   command=parent.button_run_clicked)
        
        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_message)
 
        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="Run", menu=run_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)
 

    def show_about_message(self):
        box_title = "About MicroPython Editor"
        box_message = "A simple text editor for Micro Python."
        messagebox.showinfo(box_title, box_message)
 

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 0.1 - new."
        messagebox.showinfo(box_title, box_message)