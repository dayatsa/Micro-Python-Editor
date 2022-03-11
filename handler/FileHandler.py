import os
from tkinter import filedialog


class FileHandler:
 
    @staticmethod
    def open_file():
        filename = filedialog.askopenfilename(
            defaultextension=".py",
            filetypes=[("Python Scripts", "*.py"),
                       ("All Files", "*.*"),
                       ("Text Files", "*.txt"),
                       ("Markdown Documents", "*.md"),
                       ("JavaScript Files", "*.js"),
                       ("HTML Documents", "*.html"),
                       ("CSS Documents", "*.css")])
        if filename:
            data = ""
            with open(filename, "r") as f:
                data = f.read()
            return filename, data
        else:
            return None, None
 

    @staticmethod
    def open_file_with_name(filename):
        if filename:
            data = ""
            with open(filename, "r") as f:
                data = f.read()
            return data
        else:
            return None


    @staticmethod
    def save(filename, content):
        res = False
        try:
            with open(filename, "w") as f:
                f.write(content)
            res = True
        except Exception as e:
            print(e)
        return res
 

    @staticmethod
    def save_as(content):
        res = (False, "None")
        try:
            new_filename = filedialog.asksaveasfilename(
                initialfile="Untitled.py",
                defaultextension=".py",
                filetypes=[("Python Scripts", "*.py"),
                        ("All Files", "*.*"),
                        ("Text Files", "*.txt"),
                        ("Markdown Documents", "*.md"),
                        ("JavaScript Files", "*.js"),
                        ("HTML Documents", "*.html"),
                        ("CSS Documents", "*.css")])
            with open(new_filename, "w") as f:
                f.write(content)
            res = (True, new_filename)
        except Exception as e:
            print(e)
        return res


    @staticmethod
    def check_directory_path(dir_path):
        isExist = os.path.exists(dir_path)

        if not isExist:
            # Create a new directory because it does not exist 
            os.makedirs(dir_path)
            print("The new directory is created!")
        else:
            print("Directory exist")