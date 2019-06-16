from tkinter import Tk, Frame, Button, OptionMenu, StringVar, Scrollbar, Text
from serial_interface import *

class App:
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()

        # make a scrollbar
        main_scrollbar = Scrollbar(self.frame)
        main_scrollbar.pack(side='right', fill='y')

        quit_button = Button(self.frame, text="QUIT", command=self.frame.quit)
        quit_button.pack(side="left")

        self.choices = serial_listPorts()
        self.connection_port = StringVar(root)
        if len(self.choices) == 0:
            self.choices.append(None)
        self.listports = OptionMenu(root, self.connection_port, self.choices[0], *self.choices[1:])
        self.listports.pack(side="top")

        # link function to change dropdown
        self.connection_port.trace('w', self.change_listports)

        connect = Button(self.frame, text="Connect", command=self.connect)
        connect.pack(side="top")

        disconnect = Button(self.frame, text="Disconnect", command=self.disconnect)
        disconnect.pack(side="top")

        # make a text box to put the serial output
        self.log = Text(self.frame, width=30, height=30, takefocus=0)
        self.log.pack()

        # attach text box to scrollbar
        self.log.config(yscrollcommand=main_scrollbar.set)
        main_scrollbar.config(command=self.log.yview)

        self.update_ports()

    # on change dropdown value
    def change_listports(self, *args):
        print( "Changing",self.connection_port.get() )

    def connect(self):
        print("Connection requested!")
        self.serial_instance = serial_connect(self.connection_port.get(), 115200)
        self.connection_status = serial_get_status(self.serial_instance)
        print("Connection established: ", self.serial_instance)
        self.read()

    def disconnect(self):
        print("Disconnection requested!")
        self.connection_status = serial_disconnect(self.serial_instance)

    def read(self):
        serBuffer = serial_read(self.serial_instance)
        print("Reading line: ", serBuffer)
        #add the line to the TOP of the log
        if self.connection_status:
            self.log.insert('0.0', serBuffer)
            self.frame.after(10, self.read) # check serial again soon

    def update_ports(self):
        menu = self.listports["menu"]
        new_choices = serial_listPorts()
        add_choices = set(new_choices) - set(self.choices)
        delete_choices = set(self.choices) - set(new_choices)
        self.choices = new_choices
        while len(add_choices) > 0:
            menu.add_command(label=add_choices.pop())
        while len(delete_choices) > 0:
            menu.delete(menu.index(delete_choices.pop()))

        self.frame.after(10, self.update_ports)


root = Tk()

app = App(root)

root.mainloop()

root.destroy()
