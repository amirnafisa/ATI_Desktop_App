import serial.tools.list_ports as list_ports
import serial

class ATISerial:
    def __init__(self, port, baud):
        self.port = port
        self.baud = baud
        self.instance = self.serial_connect(port, baud)
        self.serial_update_status()

    def serial_update_status(self):
        self.status = self.instance.is_open

    def serial_connect(self, port, baud):
        ser = serial.Serial(port, baud, timeout=1)

        if not ser.is_open:
            ser.open()
        if ser.is_open:
            return ser
        print("ERR: Failed to connect to port ",port," with baudrate ", baud,"...")

    def serial_disconnect(self):
        self.instance.close()
        self.serial_update_status()
        if self.status:
            print("ERR: Failed to disconnect port",self.port,"...")

    def serial_read(self):
        self.serial_update_status()
        if self.status:
            return self.instance.readline().decode('utf-8')
        else:
            print("ERR: Port ",self.port," not connected...")

def serial_listPorts():
    ports = list_ports.comports(include_links=False)
    return list(filter(lambda p: p.pid is not None, ports))

def get_port_from_device_id(device, ports):
    for p in ports:
        if p.pid == int(device):
            return p

    return None

def get_port_from_port_id(port_id, ports):
    for p in ports:
        if p.pid == port_id:
            return p

    return None
