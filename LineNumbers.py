import tkinter as tk
from tkinter import font

class LineNumbers(tk.Text):
    def __init__(self, master, text_widget, **kwargs):
        super().__init__(master, **kwargs)
 
        self.text_widget = text_widget
        self.text_widget.bind('<KeyRelease>', self.on_key_release)
        self.text_widget.bind('<FocusIn>', self.on_key_release)
        self.text_widget.bind('<MouseWheel>', self.on_key_release)
 
        self.insert(1.0, '1')
        self.configure(state='disabled')
 

    def on_key_release(self, event=None):
        p, q = self.text_widget.index("@0,0").split('.')
        p = int(p)
        final_index = str(self.text_widget.index(tk.END))
        num_of_lines = final_index.split('.')[0]
        line_numbers_string = "\n".join(str(p + no) for no in range(int(num_of_lines)))
        width = len(str(num_of_lines))
 
        self.configure(state='normal', width=width)
        self.delete(1.0, tk.END)
        self.insert(1.0, line_numbers_string)
        self.configure(state='disabled')
