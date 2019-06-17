from tkinter import Tk
from serial_interface import *
from dashboard_frame import *
from status import *

class App:
    def __init__(self, master):
        self.set_app_title(master, "ATI Interface")

        self.status = ATIStatus()

        self.main_frame = ATIDashboard(master, expand=1)
        self.menu_frame = ATIDashboard(master)
        self.status_frame = ATIDashboard(master)

        self.status_label = ATILabel(self.status_frame.frame, text='disconnected')

        log = ATILog(self.main_frame.frame, scrollbar=True)

        quit_button = ATIButton(self.menu_frame.frame, text="QUIT", btn_response=master.quit)

        connect_button = ATIButton(self.menu_frame.frame, text="Connect", btn_response=self.connect)

        disconnect_button = ATIButton(self.menu_frame.frame, text="Disconnect", btn_response=self.disconnect)

        save_session = ATIButton(self.menu_frame.frame, text="Save", btn_response=self.save)

        self.status.ports = serial_listPorts()

        choices = list(map(lambda pd: pd.device, self.status.ports))

        self.listports = ATIDropdown(self.menu_frame.frame, choices)

        self.update_ports()

    def set_app_title(self, master, title):
        top_level = master.winfo_toplevel()
        top_level.title(title)

    def connect(self):
        selected_device = self.listports.connect_variable.get()
        port = get_port_from_device_id(selected_device, self.status.ports)
        if not port:
            print("ERR: Port for device ", selected_device," not found...")
            return
        print("LOG: Connection requested to device ",port.pid," at port ",port.device,"...")

        self.serial_instance = ATISerial(port.device, 115200)

        if self.serial_instance.status:
            self.status.connection_status = True
            print("LOG: Connection established...")
            self.read()
            self.status_label.LabelUpdate(new_text='connected', new_background='green')

    def disconnect(self):
        selected_device = self.listports.connect_variable.get()
        port = get_port_from_device_id(selected_device, self.status.ports)
        if not port:
            print("ERR: Port for device ", selected_device," not found...")
            return
        print("LOG: Requesting to disconnect device ",port.pid," at port ",port.device,"...")

        serial_disconnect(self.serial_instance)

        if not self.serial_instance.status:
            self.status.connection_status = False
            self.status_label.LabelUpdate(new_text='disconnected', new_background='red')

    def read(self):
        serBuffer = self.serial_instance.serial_read()
        #add the line to the TOP of the log
        if self.serial_instance.status:
            self.log.update(serBuffer)
            if self.status.save_session and len(serBuffer) > 1:
                self.write_log2file(serBuffer)
            self.main_frame.frame.after(50, self.read) # check serial again soon

    def update_ports(self):
        old_menu = self.listports.dropdown["menu"]
        old_ports = self.status.ports
        self.status.ports = serial_listPorts()
        new_choices, old_choices = [], []
        for p in self.status.ports:
            new_choices.append(p.pid)
        for p in old_ports:
            old_choices.append(p.pid)
        add_choices = set(new_choices) - set(old_choices)
        delete_choices = set(old_choices) - set(new_choices)
        while len(add_choices) > 0:
            device = add_choices.pop()
            menu.add_command(label=device, command=lambda v=device: self.listports.connect_variable.set(v))
        while len(delete_choices) > 0:
            device = delete_choices.pop()
            selected_device = self.listports.connect_variable.get()
            menu.delete(menu.index(device))
            if selected_device == device:
                self.listports.connect_variable.set(new_choices[0])

        self.main_frame.frame.after(10, self.update_ports)

    def save(self):

        if not self.status.connection_status:
            print("ERR: No device connected...")
            return

        if not self.status.save_session:
            self.status.filename = ATISaveFile()
            port = get_port_from_port_id(self.serial_instance.port, self.status.ports)

            self.status.save_session = True

            with open(self.status.filename,'w') as f:
                f.write('Device: '+str(port.pid)+'\n')
                content=self.log.get("1.0","end")
                for line in reversed(content.split('\n')):
                    print("L:",line)
                    f.write(line)
                    f.write('\n')

    def write_log2file(self, text):
        with open(self.save_filename,'a') as f:
            print("TXT: ",text)
            f.write(text)

root = Tk()

app = App(root)

root.mainloop()

root.destroy()
