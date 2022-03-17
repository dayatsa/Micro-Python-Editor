import tkinter as tk
from tkinter import Text, Button, PhotoImage, scrolledtext
from pathlib import Path
from turtle import color
from pygments import highlight
from tkcode import CodeEditor
from tkterminal import Terminal
from handler.SerialHandler import *
from view.Menubar import Menubar
from view.Statusbar import *
from view.ResizingCanvas import *
from view.TextPad import *
import tkinter.font as tkfont
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re

from pygments.lexers.python import PythonLexer
from pygments.styles import get_style_by_name


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


class CodeView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent
        self.lexer = PythonLexer()

        # create view
        # self.root.geometry("1280x720")
        # self.root.configure(bg = "#B7C5C8")
        self.create_canvas()
        self.textarea.entry = self.auto_entry
        textScrollY = tk.Scrollbar(self.textarea, cursor="arrow", activebackground='#181B20', command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=textScrollY.set)
        textScrollY.pack(side=tk.RIGHT, fill=tk.Y)
        # self.root.bind("<KeyRelease>", self.event_key)
        
        # setting color on textarea
        # self.set_color(self.textarea)
        # self.textarea.config(tabs=tkfont.Font(font=self.textarea['font']).measure('    '))
        
        # menu
        # self.statusbar = Statusbar(self)
        # self.menubar = Menubar(self, self.root)

        # self.bind_shortcuts()


    def create_canvas(self):
        # canvas
        self.canvas = ResizingCanvas(
            self.root,
            bg = "#2C3137",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # canvas.place(x = 0, y = 0)
        self.canvas.create_rectangle(
            0.0,
            527.0,
            1280.0,
            693.0,
            fill="#181B20",
            outline="")

        self.canvas.create_text(
            1102.0,
            699.0,
            anchor="nw",
            text="Raspberry Pico on COM11",
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 12 * -1)
        )

        self.auto_entry = Label(
            self.root,
            # anchor="nw",
            text="--",
            fg="#FFFFFF",
            bg='#2C3137',
            font=("RobotoRoman Regular", 12 * -1)
        )

        auto_entry_window = self.canvas.create_window(
            14, 
            698, 
            anchor=tk.NW, 
            window=self.auto_entry)

        self.canvas.create_text(
            14.0,
            506.0,
            anchor="nw",
            text="Your File has been saved!",
            fill="#FFFFFF",
            font=("RobotoRoman Regular", 12 * -1)
        )

        self.textarea = TextPad(
            undo=True,
            maxundo=-1,
            autoseparators=True,
            bd=0,
            bg="#181B20",
            highlightthickness=0,
            padx=10,
            pady=10
        )

        textarea_window = self.canvas.create_window(
            0.0,
            69.0,
            width=1280.0,
            height=428.0,
            anchor=tk.NW, 
            window=self.textarea)

        self.canvas.create_rectangle(
            1096.0,
            13.0,
            1233.0,
            58.0,
            fill="#444B53",
            outline="#12C6FF")
        
        # print(CodeView.relative_to_assets("button_1.png"))
        self.button_image_upload = PhotoImage(
            file=CodeView.relative_to_assets("button_1.png"))
        self.button_upload = Button( 
            image=self.button_image_upload,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_upload_clicked(),
            relief="flat",
            anchor=tk.W,
            width=34.25,
            height=34.25
        )
        button_upload_window = self.canvas.create_window(
            1188.8555908203125, 
            19.088897705078125, 
            anchor=tk.NW, 
            window=self.button_upload)

        self.button_image_run = PhotoImage(
            file=CodeView.relative_to_assets("button_2.png"))
        self.button_run = Button(
            image=self.button_image_run,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_run_clicked(),
            relief="flat",
            width=34.25,
            height=34.25
        )

        button_run_window = self.canvas.create_window(
            1146.9945068359375,
            19.088897705078125,
            anchor=tk.NW, 
            window=self.button_run)


        self.button_image_stop = PhotoImage(
            file=CodeView.relative_to_assets("button_3.png"))
        self.button_stop = Button(
            image=self.button_image_stop,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_stop_clicked(),
            relief="flat",
            width=34.25,
            height=34.25
        )
        button_stop_window = self.canvas.create_window(
            1105.13330078125,
            19.088897705078125,
            anchor=tk.NW, 
            window=self.button_stop)

        self.canvas.create_rectangle(
            880.0,
            13.0,
            1065.0,
            58.0,
            fill="#444B53",
            outline="#12C6FF")

        self.canvas.create_rectangle(
            887.0,
            19.0,
            1018.0,
            52.0,
            fill="#444B53",
            outline="#969696")

        self.button_image_refresh = PhotoImage(
            file=CodeView.relative_to_assets("button_4.png"))
        self.button_refresh = Button(
            image=self.button_image_refresh,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_refresh_clicked(),
            relief="flat",
            width=33.29998779296875,
            height=33.29998779296875
        )
        button_refresh_window = self.canvas.create_window(
            1025.0400390625,
            18.91998291015625,
            anchor=tk.NW, 
            window=self.button_refresh)

        self.canvas.create_rectangle(
            27.0,
            13.0,
            182.0,
            58.0,
            fill="#444B53",
            outline="#12C6FF")

        self.button_image_save_as = PhotoImage(
            file=CodeView.relative_to_assets("button_5.png"))
        self.button_save_as = Button(
            image=self.button_image_save_as,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_save_as_clicked(),
            relief="flat",
            width=30.37445068359375,
            height=33.373199462890625
        )
        button_save_as_window = self.canvas.create_window(
            145.7978515625,
            18.933013916015625,
            anchor=tk.NW, 
            window=self.button_save_as)


        self.button_image_save = PhotoImage(
            file=CodeView.relative_to_assets("button_6.png"))
        self.button_save = Button(
            image=self.button_image_save,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_save_clicked(),
            relief="flat",
            width=30.37445068359375,
            height=33.373199462890625
        )
        button_save_window = self.canvas.create_window(
            108.67352294921875,
            18.933013916015625,
            anchor=tk.NW, 
            window=self.button_save)


        self.button_image_open_file = PhotoImage(
            file=CodeView.relative_to_assets("button_7.png"))
        self.button_open_file = Button(
            image=self.button_image_open_file,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_open_file_clicked(),
            relief="flat",
            width=30.37445068359375,
            height=33.373199462890625
        )
        button_open_file_window = self.canvas.create_window(
            71.54913330078125,
            18.933013916015625,
            anchor=tk.NW, 
            window=self.button_open_file)


        self.button_image_new_file = PhotoImage(
            file=CodeView.relative_to_assets("button_8.png"))
        self.button_new_file = Button(
            image=self.button_image_new_file,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.button_new_file_clicked(),
            relief="flat",
            width=30.37445068359375,
            height=33.373199462890625
        )
        button_new_file_window = self.canvas.create_window(
            34.4249267578125,
            18.933013916015625,
            anchor=tk.NW, 
            window=self.button_new_file)



        # self.canvas = Canvas(
        #     self.root,
        #     bg = "#B7C5C8",
        #     height = 720,
        #     width = 1280,
        #     bd = 0,
        #     highlightthickness = 0,
        #     relief = "ridge"
        # )
        # self.canvas.place(x = 0, y = 0)
        # # terminal
        # self.terminal = Terminal(pady=5, padx=5)
        # self.terminal.shell = True
        # self.terminal.place(
        #     x=895.0,
        #     y=90.0,
        #     width=370.0,
        #     height=614.0
        # )
        # # background textarea
        # self.entry_image_1 = PhotoImage(
        #     file=CodeView.relative_to_assets("entry_1.png"))
        # entry_bg_1 = self.canvas.create_image(
        #     447.5,
        #     398.0,
        #     image=self.entry_image_1
        # )
        # #textarea
        # self.textarea = Text(
        #     bd=0,
        #     bg="#FFFFFF",
        #     highlightthickness=0
        # )
        # self.textarea.place(
        #     x=25.0,
        #     y=90.0,
        #     width=845.0,
        #     height=614.0
        # )
        # # scroolbar on textarea
        # self.scroll = tk.Scrollbar(self.root, command=self.textarea.yview)
        # self.textarea.configure(yscrollcommand=self.scroll.set)
        # self.scroll.place(
        #     x=865,
        #     y=90,
        #     height=600
        # )
        # #text
        # self.canvas.create_text(
        #     27.0,
        #     23.0,
        #     anchor="nw",
        #     text="MicroPython",
        #     fill="#0092B2",
        #     font=("RobotoRoman Bold", 30 * -1)
        # )
        # #text
        # self.canvas.create_text(
        #     29.0,
        #     55.0,
        #     anchor="nw",
        #     text="Editor",
        #     fill="#37A2B9",
        #     font=("RobotoRoman SemiBold", 14 * -1)
        # )
        # # button run
        # self.button_image_1 = PhotoImage(
        #     file=CodeView.relative_to_assets("button_1.png"))
        # self.button_run = Button(
        #     image=self.button_image_1,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.button_run_clicked(),
        #     relief="flat"
        # )
        # self.button_run.place(
        #     x=1172.0,
        #     y=31.0,
        #     width=90.0,
        #     height=40.0
        # )
        # # button new file
        # self.button_image_2 = PhotoImage(
        #     file=CodeView.relative_to_assets("button_2.png"))
        # self.button_new_file = Button(
        #     image=self.button_image_2,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.button_new_file_clicked(),
        #     relief="flat"
        # )
        # self.button_new_file.place(
        #     x=268.0,
        #     y=31.0,
        #     width=90.0,
        #     height=40.0
        # )
        # # button open file
        # self.button_image_3 = PhotoImage(
        #     file=CodeView.relative_to_assets("button_3.png"))
        # self.button_open_file = Button(
        #     image=self.button_image_3,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.button_open_file_clicked(),
        #     relief="flat"
        # )
        # self.button_open_file.place(
        #     x=377.0,
        #     y=31.0,
        #     width=90.0,
        #     height=40.0
        # )
        # # button save
        # self.button_image_4 = PhotoImage(
        #     file=CodeView.relative_to_assets("button_4.png"))
        # self.button_save = Button(
        #     image=self.button_image_4,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.button_save_clicked(),
        #     relief="flat"
        # )
        # self.button_save.place(
        #     x=486.0,
        #     y=31.0,
        #     width=90.0,
        #     height=40.0
        # )
        # # button refresh
        # self.button_refresh = Button(
        #     self.root,
        #     text="Refresh",
        #     command=self.button_refresh_clicked
        # )
        # self.button_refresh.place(
        #     x=900,
        #     y=40,
        #     width=90,
        #     height=30
        # )
        # # button stop
        # self.button_stop = Button(
        #     self.root,
        #     text="Stop",
        #     command=self.button_stop_clicked
        # )
        # self.button_stop.place(
        #     x=1100,
        #     y=40,
        #     width=60,
        #     height=30
        # )
        # # option list COM
        # self.variable_com = tk.StringVar(self.root)
        # self.list_com = tk.OptionMenu(self.root, self.variable_com, *SerialHandler.get_list_ports())
        # self.list_com.place(
        #     x=1000,
        #     y=40,
        #     width=90,
        #     height=30
        # )


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

    
    def button_upload_clicked(self, *args):
        if self.controller:
            self.controller.upload()


    def set_window_title(self, name=None):
        if name:
            self.root.title(name + " - MicroPython Editor")
        else:
            self.root.title("Untitled - MicroPython Editor")
        

    def button_stop_clicked(self):
        if self.controller:
            self.controller.stop_run()


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

