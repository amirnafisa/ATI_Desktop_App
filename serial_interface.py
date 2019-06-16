import serial.tools.list_ports as list_ports
import serial

def serial_listPorts():
    ports = list(map(lambda p:p.device, list_ports.comports(include_links=False)))
    print("Found following ports connected: ", ports)
    return ports

def serial_get_status(ser_instance):
    return ser_instance.is_open

def serial_connect(port, baud):
    ser = serial.Serial(port, baud, timeout=1)
    if not ser.is_open:
        ser.open()
    if ser.is_open:
        return ser
    return False

def serial_disconnect(ser_instance):
    ser_instance.close()
    return ser_instance.is_open

def serial_read(ser_instance):
    if ser_instance.is_open:
        return ser_instance.readline()
