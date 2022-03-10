import tkinter as tk 
from model.CodeModel import *
from controller.CodeController import *
from view.CodeView import *


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Micro Python Editor')

        # create a model
        model = CodeModel("None")

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