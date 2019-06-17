from tkinter import Frame, Button, OptionMenu, StringVar, Scrollbar, Text, Label, filedialog
from style import *

class ATIDashboard:
    def __init__ (self, master, expand=0):
        self.frame = Frame(master)
        self.frame.pack(side='top',fill='both', expand=expand)

class ATIButton:
    def __init__ (self, master, text, btn_response):
        self.button = Button(master, text=text, command=btn_response, style=style_button())
        self.button.pack(side="left")

class ATIScroll:
    def __init__ (self, master):
        self.scrollbar = Scrollbar(master)
        self.scrollbar.pack(side='right', fill='y')

class ATILabel:
    def __init__ (self, master, text='', background='white'):
        self.text = text
        self.background = background
        self.label = Label(master, text=text)
        self.label.pack(side='bottom')

    def LabelUpdate(self, new_text=False, new_background=False):
        new_text = self.text if not new_text else new_text
        new_background = self.background if not new_background else new_background
        self.label.configure(text=new_text, background=new_background)

class ATILog:
    def __init__(self, master, state='disabled', scrollbar=False):
        # make a text box to put the serial output
        self.log = Text(master)

        if scrollbar:
            scrollbar = ATIScroll(self.log)

            # attach text box to scrollbar
            self.log.config(yscrollcommand=scrollbar.scrollbar.set)
            scrollbar.scrollbar.config(command=self.log.yview)

        self.log.pack(fill='both', expand=1)

    def update(self, text):
        self.log.insert('0.0', text)

class ATIDropdown:
    def __init__(self, master, menu):
        self.connect_variable = StringVar(master)

        self.dropdown = OptionMenu(master, self.connect_variable, *menu if menu else '0')
        # link function to change dropdown
        self.connect_variable.trace('w', self.update_choices)
        self.dropdown.pack(side="left")

    # on change dropdown value
    def update_choices(self, *args):
        print( "LOG: Changing selection to ",self.connect_variable.get(),"..." )

def ATISaveFile():
    filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file")
    return filename
