from fileinput import filename
import tkinter as tk
from handler.FileHandler import *
from handler.SerialHandler import *


class CodeController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # variable view



    def new_file(self, *args):
        # clear model
        self.model.set_filename(None)
        self.model.set_code("")
        # clear view
        self.view.textarea.delete(1.0, tk.END)
        self.view.set_window_title()
 

    def open_file(self, *args):
        filename, data = FileHandler.open_file()
        if filename is not None:
            # set model
            self.model.set_filename(filename)
            self.model.set_code(data)
            # set view
            self.view.textarea.delete(1.0, tk.END)
            self.view.textarea.insert(1.0, self.model.get_code())
            self.view.set_window_title(self.model.get_filename())
 

    def save(self, *args):
        self.model.set_code(self.view.textarea.get(1.0, tk.END))
        res = FileHandler.save(self.model.get_filename(), self.model.get_code())
        if res:
            self.view.statusbar.update_status(True)
            self.view.set_window_title(self.model.get_filename())
        else:
            self.save_as()
 

    def save_as(self, *args):
        self.model.set_code(self.view.textarea.get(1.0, tk.END))
        res, filename = FileHandler.save_as(self.model.get_code())
        if res:
            self.view.statusbar.update_status(True)
            self.model.set_filename(filename)
            self.set_window_title(self.model.get_filename())


    def run_code(self, *args):
        self.save()

        self.view.statusbar.update_status("Running Code..")
        # print("running on " + self.variable_com.get())
        # self.terminal.run_command("ampy --port " + self.variable_com.get() + " put " + str(self.filename))       
        # self.terminal.clear()
        # time.sleep(0.1)
        # self.terminal.run_command("ampy --port " + self.variable_com.get() + " run " + str(self.file_handler.get_filename()))
 

    def stop_run(self):
        print("stop running")
        try:
            self.terminal.run_command('taskkill /IM "ampy.exe" /F')
        except Exception as e:
            print(e)


    def refresh(self):
        self.option_list_com = SerialHandler.get_list_ports()
        menu = self.view.list_com["menu"]
        menu.delete(0, "end")
        for string in self.option_list_com:
            menu.add_command(label=string, 
                             command=lambda value=string: self.view.variable_com.set(value))


    