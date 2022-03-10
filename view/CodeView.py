import tkinter as tk
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
from pathlib import Path
from tkterminal import Terminal
from handler.SerialHandler import *
from view.Menubar import Menubar
from view.Statusbar import *
import tkinter.font as tkfont
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


class CodeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent

        # create view
        self.root.geometry("1280x720")
        self.root.configure(bg = "#B7C5C8")
        self.create_canvas()
        
        # setting color on textarea
        self.set_color(self.textarea)
        self.textarea.config(tabs=tkfont.Font(font=self.textarea['font']).measure('    '))
        
        # menu
        self.statusbar = Statusbar(self)
        self.menubar = Menubar(self, self.root)

        self.bind_shortcuts()


    def create_canvas(self):
        # canvas
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
        # terminal
        self.terminal = Terminal(pady=5, padx=5)
        self.terminal.shell = True
        self.terminal.place(
            x=895.0,
            y=90.0,
            width=370.0,
            height=614.0
        )
        # background textarea
        self.entry_image_1 = PhotoImage(
            file=CodeView.relative_to_assets("entry_1.png"))
        entry_bg_1 = self.canvas.create_image(
            447.5,
            398.0,
            image=self.entry_image_1
        )
        #textarea
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
        # scroolbar on textarea
        self.scroll = tk.Scrollbar(self.root, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.scroll.place(
            x=865,
            y=90,
            height=600
        )
        #text
        self.canvas.create_text(
            27.0,
            23.0,
            anchor="nw",
            text="MicroPython",
            fill="#0092B2",
            font=("RobotoRoman Bold", 30 * -1)
        )
        #text
        self.canvas.create_text(
            29.0,
            55.0,
            anchor="nw",
            text="Editor",
            fill="#37A2B9",
            font=("RobotoRoman SemiBold", 14 * -1)
        )
        # button run
        self.button_image_1 = PhotoImage(
            file=CodeView.relative_to_assets("button_1.png"))
        self.button_run = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_run_clicked(),
            relief="flat"
        )
        self.button_run.place(
            x=1172.0,
            y=31.0,
            width=90.0,
            height=40.0
        )
        # button new file
        self.button_image_2 = PhotoImage(
            file=CodeView.relative_to_assets("button_2.png"))
        self.button_new_file = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_new_file_clicked(),
            relief="flat"
        )
        self.button_new_file.place(
            x=268.0,
            y=31.0,
            width=90.0,
            height=40.0
        )
        # button open file
        self.button_image_3 = PhotoImage(
            file=CodeView.relative_to_assets("button_3.png"))
        self.button_open_file = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_open_file_clicked(),
            relief="flat"
        )
        self.button_open_file.place(
            x=377.0,
            y=31.0,
            width=90.0,
            height=40.0
        )
        # button save
        self.button_image_4 = PhotoImage(
            file=CodeView.relative_to_assets("button_4.png"))
        self.button_save = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_save_clicked(),
            relief="flat"
        )
        self.button_save.place(
            x=486.0,
            y=31.0,
            width=90.0,
            height=40.0
        )
        # button refresh
        self.button_refresh = Button(
            self.root,
            text="Refresh",
            command=self.button_refresh_clicked
        )
        self.button_refresh.place(
            x=900,
            y=40,
            width=90,
            height=30
        )
        # button stop
        self.button_stop = Button(
            self.root,
            text="Stop",
            command=self.button_stop_clicked
        )
        self.button_stop.place(
            x=1100,
            y=40,
            width=60,
            height=30
        )
        # option list COM
        self.variable_com = tk.StringVar(self.root)
        self.list_com = tk.OptionMenu(self.root, self.variable_com, SerialHandler.get_list_ports())
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
    

    def set_controller(self, controller):
        self.controller = controller

    
    def button_run_clicked(self, *args):
        if self.controller:
            self.controller.run_code()


    def button_new_file_clicked(self, *args):
        if self.controller:
            self.controller.new_file()


    def button_open_file_clicked(self, *args):
        if self.controller:
            self.controller.open_file()
        

    def button_save_clicked(self, *args):
        if self.controller:
            self.controller.save()

    
    def button_save_as_clicked(self, *args):
        if self.controller:
            self.controller.save_as()


    def button_refresh_clicked(self, *args):
        if self.controller:
            self.controller.refresh()


    def button_stop_clicked(self, *args):
        if self.controller:
            self.controller.stop_run()


    def set_window_title(self, name=None):
        if name:
            self.root.title(name + " - MicroPython Editor")
        else:
            self.root.title("Untitled - MicroPython Editor")
        

    def button_stop_clicked(self):
        if self.controller:
            self.controller.save()


    def bind_shortcuts(self):
        self.textarea.bind('<Control-n>', self.button_new_file_clicked)
        self.textarea.bind('<Control-o>', self.button_open_file_clicked)
        self.textarea.bind('<Control-s>', self.button_save_clicked)
        # self.textarea.bind('<Control-S>', self.button_save_clicked)
        # self.view.textarea.bind('<Key>', self.statusbar.update_status)
        self.textarea.bind('<Control-r>', self.button_run_clicked)



    @staticmethod
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

