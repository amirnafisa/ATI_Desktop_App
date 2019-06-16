from tkinter import Tk, Frame, Button, OptionMenu, StringVar, Scrollbar, Text, Label
from serial_interface import *
from main_app_features import *

class App:
    def __init__(self, master):
        set_app_title(master, "ATI Interface")

        self.saving_status = False

        self.frame = Frame(master)
        self.frame.pack()

        self.status_label = Label(self.frame, text='disconnected')
        self.status_label.pack(side='bottom')

        # make a scrollbar
        main_scrollbar = Scrollbar(self.frame)
        main_scrollbar.pack(side='right', fill='y')

        quit_button = Button(self.frame, text="QUIT", command=self.frame.quit)
        quit_button.pack(side="left")

        self.ports = serial_listPorts()
        choices = []
        for p in self.ports:
            choices.append(p['serial_number'])
        self.connection_device = StringVar(root)
        if len(choices) == 0:
            choices.append(None)
        self.listports = OptionMenu(root, self.connection_device, choices[0], *choices[1:])
        self.listports.pack(side="top")

        # link function to change dropdown
        self.connection_device.trace('w', self.change_listports)

        connect = Button(self.frame, text="Connect", command=self.connect)
        connect.pack(side="top")

        disconnect = Button(self.frame, text="Disconnect", command=self.disconnect)
        disconnect.pack(side="top")

        save_session = Button(self.frame, text="Save", command=self.save)
        save_session.pack(side="top")

        # make a text box to put the serial output
        self.log = Text(self.frame)
        self.log.pack()

        # attach text box to scrollbar
        self.log.config(yscrollcommand=main_scrollbar.set)
        main_scrollbar.config(command=self.log.yview)

        self.update_ports()

    # on change dropdown value
    def change_listports(self, *args):
        print( "Changing",self.connection_device.get() )

    def connect(self):

        selected_device = self.connection_device.get()
        port = None
        for p in self.ports:
            if int(p['serial_number']) == int(selected_device):
                port = p['port_no']
                break
        print("Connection requested!",selected_device,port)
        self.serial_instance = serial_connect(port, 115200)
        self.connection_status = serial_get_status(self.serial_instance)
        print("Connection established: ", self.serial_instance)
        self.read()
        if serial_get_status(self.serial_instance):
            self.status_label['text'] = 'connected'

    def disconnect(self):
        print("Disconnection requested!")
        self.connection_status = serial_disconnect(self.serial_instance)
        if not serial_get_status(self.serial_instance):
            self.status_label['text'] = 'disconnected'

        print("Printint text",self.log.get("1.0","end"))

    def read(self):
        serBuffer = serial_read(self.serial_instance)
        #add the line to the TOP of the log
        if self.connection_status:
            self.log.insert('0.0', serBuffer)
            if self.saving_status and len(str(serBuffer)) > 5:
                self.write_log2file(self.log.get('current linestart','current lineend'))
            self.frame.after(50, self.read) # check serial again soon

    def update_ports(self):
        menu = self.listports["menu"]
        available_ports = serial_listPorts()
        new_choices, old_choices = [], []
        for p in available_ports:
            new_choices.append(p['serial_number'])
        for p in self.ports:
            old_choices.append(p['serial_number'])
        add_choices = set(new_choices) - set(old_choices)
        delete_choices = set(old_choices) - set(new_choices)
        while len(add_choices) > 0:
            menu.add_command(label=add_choices.pop())
        while len(delete_choices) > 0:
            menu.delete(menu.index(delete_choices.pop()))

        self.ports = available_ports

        self.frame.after(10, self.update_ports)

    def save(self):
        if not self.saving_status:
            device = 0
            for p in self.ports:
                if p['port_no'] == self.serial_instance.port:
                    device = p['serial_number']
                    break
            self.saving_status = True
            self.save_filename = get_file_name()
            with open(self.save_filename,'w') as f:
                f.write('Device: '+str(device)+'\n')
                f.write(self.log.get("1.0","end"))
                f.write('\n')


    def write_log2file(self, text):
        with open(self.save_filename,'a') as f:
            f.write(text)
            f.write('\n')

root = Tk()

app = App(root)

root.mainloop()

root.destroy()
