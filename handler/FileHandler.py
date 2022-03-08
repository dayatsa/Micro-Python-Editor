import os
from tkinter import filedialog


class FileHandler:

    def __init__(self):
        self.__filename = None

    
    def get_filename(self):
        return self.__filename


    def new_file(self, *args):
        self.__filename = None
 

    def open_file(self, *args):
        self.__filename = filedialog.askopenfilename(
            defaultextension=".py",
            filetypes=[("Python Scripts", "*.py"),
                       ("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if self.__filename:
            data = ""
            with open(self.__filename, "r") as f:
                data = f.read()
            return data
        else:
            return None
 

    def save(self, content):
        res = False
        try:
            with open(self.__filename, "w") as f:
                f.write(content)
            res = True
        except Exception as e:
            print(e)
        return res
 

    def save_as(self, content):
        res = False
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.py",
                defaultextension=".py",
                filetypes=[("Python Scripts", "*.py"),
                        ("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            with open(new_file, "w") as f:
                f.write(content)
            self.__filename = new_file
            res = True
        except Exception as e:
            print(e)
        return res
