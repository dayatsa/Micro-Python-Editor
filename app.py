import tkinter as tk
from ttkthemes import ThemedTk
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

        # setting path
        path = os.path.join(OUTPUT_PATH, "micropython_lib")
        path_code = os.path.join(OUTPUT_PATH, "res")
        
        # get code on library
        lib = LibraryHandler.get_library_code(os.path.join(path, "micropython"))
        template = LibraryHandler.get_template_code(os.path.join(path, "template.py"))
        
        # check path directory
        FileHandler.check_directory_path(path_code)
        
        # create a model        
        model = CodeModel(header=lib, 
                        path_lib=path_code,
                        template=template)

        # create a view and place it on the root window
        view = CodeView(self)

        # create a controller
        # controller = CodeController(model, view)

        # set the controller to view
        # view.set_controller(controller)


if __name__ == '__main__':
    app = App()
    app.mainloop()