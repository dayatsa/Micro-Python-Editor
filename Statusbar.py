from ast import arg
import tkinter as tk
from tokenize import String

class Statusbar:
 
    def __init__(self, parent):
 
        font_specs = ("ubuntu", 10)
 
        self.status = tk.StringVar()
        self.status.set("MicroPython Editor v1.0")
 
        label = tk.Label(parent.textarea, textvariable=self.status, fg="black",
                         bg="lightgrey", anchor='sw', font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)
 
    def update_status(self, *args):
        if isinstance(args[0], bool):
            self.status.set("Your File Has Been Saved!")
        elif isinstance(args[0], str):
            self.status.set(args[0])
        else:
            self.status.set("MicroPython Editor")