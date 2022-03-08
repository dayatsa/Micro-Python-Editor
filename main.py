from fileinput import filename
from msilib.schema import Error
from pathlib import Path
import signal
import tkinter.font as tkfont
import idlelib.colorizer as ic
import idlelib.percolator as ip
import time
import re
import os
from tkterminal import Terminal

from handler.FileHandler import *
from Menubar import *
from Statusbar import *
from LineNumbers import *

"""
ampy-adafruit
pyserial
"""


# from tkinter import *
# Explicit imports to satisfy Flake8
# import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class TextEditor:
    
    def __init__(self, root):
        self.filename = None

        self.root = root
        self.root.geometry("1280x720")
        self.root.configure(bg = "#B7C5C8")
        self.create_canvas()
        # text area
        self.set_color(self.textarea)
        self.textarea.config(tabs=tkfont.Font(font=self.textarea['font']).measure('    '))
 
        self.terminal_reset = Terminal(pady=5, padx=5)
        # menubar and status bar
        self.menubar = Menubar(self)
        self.statusbar = Statusbar(self)
        self.file_handler = FileHandler()
        self.bind_shortcuts()

        
    def create_canvas(self):
        self.canvas = Canvas(
            self.root,
            bg = "#B7C5C8",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)

        self.terminal = Terminal(pady=5, padx=5)
        self.terminal.shell = True
        self.terminal.place(
            x=895.0,
            y=90.0,
            width=370.0,
            height=614.0
        )

        # self.canvas.create_rectangle(
        #     895.0,
        #     90.0,
        #     1262.0,
        #     706.0,
        #     fill="#FFFFFF",
        #     outline="")

        self.entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            447.5,
            398.0,
            image=self.entry_image_1
        )

        self.textarea = Text(
            bd=0,
            bg="#FFFFFF",
            highlightthickness=0
        )
        self.textarea.place(
            x=25.0,
            y=90.0,
            width=845.0,
            height=614.0
        )
        self.scroll = tk.Scrollbar(self.root, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(
            x=865,
            y=90,
            height=600
        )

        # self.line_number = LineNumbers(self.root, self.textarea, width=1)
        # self.line_number.place(
        #     x=20,
        #     y=90,
        #     height=600
        # )

        self.canvas.create_text(
            27.0,
            23.0,
            anchor="nw",
            text="MicroPython",
            fill="#0092B2",
            font=("RobotoRoman Bold", 30 * -1)
        )

        self.canvas.create_text(
            29.0,
            55.0,
            anchor="nw",
            text="Editor",
            fill="#37A2B9",
            font=("RobotoRoman SemiBold", 14 * -1)
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.run_code(),
            relief="flat"
        )
        self.button_1.place(
            x=1172.0,
            y=31.0,
            width=90.0,
            height=40.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.new_file_text(),
            relief="flat"
        )
        self.button_2.place(
            x=268.0,
            y=31.0,
            width=90.0,
            height=40.0
        )

        self.button_image_3 = PhotoImage(
            file=relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.open_file_text(),
            relief="flat"
        )
        self.button_3.place(
            x=377.0,
            y=31.0,
            width=90.0,
            height=40.0
        )

        self.button_image_4 = PhotoImage(
            file=relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.save_text(),
            relief="flat"
        )
        self.button_4.place(
            x=486.0,
            y=31.0,
            width=90.0,
            height=40.0
        )

        self.button_refresh = Button(
            self.root,
            text="Refresh",
            command=self.refresh
        )
        self.button_refresh.place(
            x=900,
            y=40,
            width=90,
            height=30
        )

        self.button_stop = Button(
            self.root,
            text="Stop",
            command=self.stop_run
        )
        self.button_stop.place(
            x=1100,
            y=40,
            width=60,
            height=30
        )

        self.option_list_com = self.list_ports()
        self.variable_com = tk.StringVar(self.root)
        
        self.list_com = tk.OptionMenu(self.root, self.variable_com, *self.option_list_com)
        self.list_com.place(
            x=1000,
            y=40,
            width=90,
            height=30
        )
    
    def set_color(self, text):
        cdg = ic.ColorDelegator()
        cdg.prog = re.compile(r'\b(?P<MYGROUP>tkinter)\b|' + ic.make_pat(), re.S)
        cdg.idprog = re.compile(r'\s+(\w+)', re.S)
        cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F', 'background': '#FFFFFF'}
        # These five lines are optional. If omitted, default colours are used.
        cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
        cdg.tagdefs['KEYWORD'] = {'foreground': '#007F00', 'background': '#FFFFFF'}
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}
        ip.Percolator(text).insertfilter(cdg)

    
    def set_window_title(self, name=None):
        if name:
            self.root.title(name + " - MicroPython Editor")
        else:
            self.root.title("Untitled - MicroPython Editor")
 

    def new_file_text(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.set_window_title()
        self.file_handler.new_file()
 

    def open_file_text(self, *args):
        data = self.file_handler.open_file()
        if data is not None:
            self.textarea.delete(1.0, tk.END)
            self.textarea.insert(1.0, data)
            self.set_window_title(self.file_handler.get_filename())
 

    def save_text(self, *args):
        res = self.file_handler.save(self.textarea.get(1.0, tk.END))
        if res:
            self.statusbar.update_status(True)
            self.set_window_title(self.file_handler.get_filename())
        else:
            self.save_as_text()
 

    def save_as_text(self, *args):
        res = self.file_handler.save_as(self.textarea.get(1.0, tk.END))
        if res:
            self.statusbar.update_status(True)
            self.set_window_title(self.file_handler.get_filename())


    def run_code(self, *args):
        self.save_text()

        self.statusbar.update_status("Running Code..")
        print("running on " + self.variable_com.get())
        # self.terminal.run_command("ampy --port " + self.variable_com.get() + " put " + str(self.filename))       
        self.terminal.clear()
        time.sleep(0.1)
        self.terminal.run_command("ampy --port " + self.variable_com.get() + " run " + str(self.file_handler.get_filename()))
 

    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.new_file_text)
        self.textarea.bind('<Control-o>', self.open_file_text)
        self.textarea.bind('<Control-s>', self.save_text)
        self.textarea.bind('<Control-S>', self.save_as_text)
        self.textarea.bind('<Key>', self.statusbar.update_status)
        self.textarea.bind('<Control-r>', self.run_code)


    def stop_run(self):
        print("stop running")
        try:
            self.terminal.run_command('taskkill /IM "ampy.exe" /F')
        except Exception as e:
            print(e)

    def refresh(self):
        self.option_list_com = self.list_ports()
        # print("ampy --port " + self.variable_com.get() + " reset")
        menu = self.list_com["menu"]
        menu.delete(0, "end")
        for string in self.option_list_com:
            menu.add_command(label=string, 
                             command=lambda value=string: self.variable_com.set(value))


    def list_ports(self):
        # Find and return a list of all EiBotBoard units
        # connected via USB port.
        try:
            from serial.tools.list_ports import comports
        except ImportError():
            return ["None"]
            print("import error")
        
        if comports:
            com_ports_list = list(comports())
            # print(com_ports_list)
            ebb_ports_list = []
            for port in com_ports_list:
                port_has_ebb = False
                if port[1].startswith("USB"):
                    port_has_ebb = True
                elif port[2].startswith("USB VID:PID"):
                    port_has_ebb = True
                if port_has_ebb:
                    ebb_ports_list.append(port[0])
            if len(ebb_ports_list) == 0:
                return ['None']
            else:
                return ebb_ports_list 


if __name__ == "__main__":
    root = Tk()
    pt = TextEditor(root)
    root.mainloop()
