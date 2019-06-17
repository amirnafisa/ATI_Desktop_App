from tkinter.ttk import *

def style_button():
    style = Style()

    btn_style = 'W.TButton'
    style.configure(btn_style, font =
               ('calibri', 10, 'bold'),
                foreground = 'red', highlightbackground = 'green')


    return btn_style
