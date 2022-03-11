import tkinter as tk
from handler.LibraryHandler import LibraryHandler 
from model.CodeModel import *
from controller.CodeController import *
from view.CodeView import *
from pathlib import Path
import os


OUTPUT_PATH = Path(__file__).parent


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Micro Python Editor')

        # create a model
        path = os.path.join(OUTPUT_PATH, "micropython_lib")
        lib = LibraryHandler.get_library_code(path)
        path_code = os.path.join(OUTPUT_PATH, "res")
        FileHandler.check_directory_path(path_code)
        model = CodeModel(header=lib, code="None", path_lib=path_code)

        # create a view and place it on the root window
        view = CodeView(self)
        # view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = CodeController(model, view)

        # set the controller to view
        view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()