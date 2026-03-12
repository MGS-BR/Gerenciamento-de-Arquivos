from tkinter import *
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, msg):
        self.widget.insert(END, msg)
        self.widget.see(END)

    def flush(self):
        pass

class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        

root = Tk()
root.title("Conntador")
Application(root)
root.mainloop()