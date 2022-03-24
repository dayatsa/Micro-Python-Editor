import tkinter as tk
import time
import os
from fileinput import filename
from handler.FileHandler import *
from handler.SerialHandler import *


class CodeController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.new_file()
        self.refresh()


    def new_file(self, *args):
        # clear model
        self.model.set_filename(None)
        self.model.reset_code()
        # clear view
        self.view.reset_content_textarea()
        self.view.set_content_textarea(self.model.get_code())
        self.view.set_window_title()
        self.view.set_statusbar("Success creating new file!")
        print("Create new file")
 

    def open_file(self, *args):
        filename, data = FileHandler.open_file()
        if filename is not None:
            # set model
            self.model.set_filename(filename)
            self.model.set_code(data)
            # set view
            self.view.reset_content_textarea()
            self.view.set_content_textarea(self.model.get_code())
            self.view.set_window_title(self.model.get_filename())
            self.view.set_statusbar("Success open " + self.model.get_filename())
 
    
    def open_file_with_name(self, path, filename):
        data = FileHandler.open_file_with_name(os.path.join(path, filename))
        if data is not None:
            # set model
            self.model.set_filename(None)
            self.model.set_code(data)
            # set view
            self.view.reset_content_textarea()
            self.view.set_content_textarea(self.model.get_code())
            self.view.set_window_title()
            self.view.set_statusbar("Success open " + filename)


    def save(self, *args):
        self.model.set_code(self.view.get_content_textarea())
        res = FileHandler.save(self.model.get_filename(), self.model.get_code())
        if res:
            self.view.set_statusbar(True)
            self.view.set_window_title(self.model.get_filename())
        else:
            self.save_as()
 

    def save_as(self, *args):
        self.model.set_code(self.view.get_content_textarea())
        res, filename = FileHandler.save_as(self.model.get_code())
        if res:
            self.view.set_statusbar(True)
            self.model.set_filename(filename)
            self.view.set_window_title(self.model.get_filename())

    
    def save_main_code(self, *args):
        if os.path.exists(self.model.get_path_main_code()):
            os.remove(self.model.get_path_main_code())
            print("Delete the file")
        else:
            print("Can not delete the file as it doesn't exists")
        self.model.set_code(self.view.get_content_textarea())
        res = FileHandler.save(self.model.get_path_main_code(), self.model.get_full_code())
        return res


    def run_code(self, *args):
        self.save()
        self.save_main_code()

        self.view.set_statusbar("Running Code..")
        print("running on " + self.view.get_port_selected() + " port")
        print(str(self.model.get_path_main_code()))
        self.view.terminal.clear()
        time.sleep(0.1)
        self.view.terminal.run_command("ampy --port " + self.view.get_port_selected() + " run " + str(self.model.get_path_main_code()))
 

    def upload(self, *args):
        self.save()
        self.save_main_code()

        self.view.set_statusbar("Uploading Code..")
        print("uploading on " + self.view.get_port_selected())
        print(str(self.model.get_path_main_code()))
        self.view.terminal.clear()
        self.view.terminal.run_command("ampy --port " + self.view.get_port_selected() + " put " + str(self.model.get_path_main_code()))       
        

    def stop_run(self):
        print("stop running")
        try:
            self.view.terminal.run_command('taskkill /IM "ampy.exe" /F')
        except Exception as e:
            print(e)


    def refresh(self):
        self.option_list_com = SerialHandler.get_list_ports()
        menu = self.view.list_com["menu"]
        menu.delete(0, "end")
        for string in self.option_list_com:
            menu.add_command(label=string, 
                             command=lambda value=string: self.view.option_menu_clicked(value))

    
    def on_click_option_list(self, value):
        print(value)

    