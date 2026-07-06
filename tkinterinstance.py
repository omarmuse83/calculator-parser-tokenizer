from tkinter import Tk, StringVar, Button, Label, Entry, N, END
import string

class TkinterInstance(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('tkinter-custom-parser')
        self.config(bg='#f2f2f2')
        self.minsize(width=400, height=500)
        self.maxsize(width=1100, height=900)
        self.resizable(0, 0)


    
    