from tkinter import *


class StatusBar(Frame):
    height = 19  # 19 for the label, 1 for the top and 1 for the bottom border

    def __init__(self, master):
        Frame.__init__(self, master)
        self.label = Label(self, bd=1, relief=SUNKEN, anchor=W)
        self.label.pack(fill=BOTH)

    def set(self, format_str, *args):
        self.label.config(text=format_str % args)
        self.label.update_idletasks()

    def clear(self):
        self.label.config(text="")
        self.label.update_idletasks()
