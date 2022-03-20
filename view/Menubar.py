from cProfile import label
import tkinter as tk
import os
from tkinter import messagebox

from click import command

class Menubar:
    def __init__(self, parent, root, path_example):
        self.parent = parent
        font_specs = ("Helvetica", 10)
 
        self.menubar = tk.Menu(root, font=font_specs)
        root.config(menu=self.menubar)
 
        file_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File",
                                  accelerator="Ctrl+N",
                                  command=self.parent.button_new_file_clicked)
        file_dropdown.add_command(label="Open File",
                                  accelerator="Ctrl+O",
                                  command=self.parent.button_open_file_clicked)
        file_dropdown.add_command(label="Save",
                                  accelerator="Ctrl+S",
                                  command=self.parent.button_save_clicked)
        file_dropdown.add_command(label="Save As",
                                  accelerator="Ctrl+Shift+S",
                                  command=self.parent.button_save_as_clicked)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit",
                                  command=root.destroy)
 
        run_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        run_dropdown.add_command(label="Run Code",
                                accelerator="Ctrl+R",
                                   command=self.parent.button_run_clicked)
        
        about_dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                   command=self.show_release_notes)
        about_dropdown.add_separator()
        about_dropdown.add_command(label="About",
                                   command=self.show_about_message)

        example_dropdown = self.create_example_menu(font_specs, path_example)
 
        self.menubar.add_cascade(label="File", menu=file_dropdown)
        self.menubar.add_cascade(label="Example", menu=example_dropdown)
        self.menubar.add_cascade(label="Run", menu=run_dropdown)
        self.menubar.add_cascade(label="About", menu=about_dropdown)


    def create_example_menu(self, font_specs, path_example):
        dropdown = tk.Menu(self.menubar, font=font_specs, tearoff=0)

        self.menu_example = []
        list_dir = os.listdir(path_example)
        for i in range(len(list_dir)):
            path_dir = os.path.join(path_example, list_dir[i])
            self.menu_example.append(tk.Menu(self.menubar, font=font_specs, tearoff=0))

            for name in os.listdir(path_dir):
                self.menu_example[i].add_command(label=name, command=lambda p=path_dir,n=name: self.example_menu_command(p, n))

            dropdown.add_cascade(label=list_dir[i], menu=self.menu_example[i])

        return dropdown

    def example_menu_command(self, path, name):
        self.parent.on_examplebar_clicked(path, name)

    def show_about_message(self):
        box_title = "About MicroPython Editor"
        box_message = "A simple text editor for Micro Python."
        messagebox.showinfo(box_title, box_message)
 

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 0.1 - new."
        messagebox.showinfo(box_title, box_message)