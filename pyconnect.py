import serial
import snap7
from snap7.util import *
from snap7.snap7types import *

class Arduino():
    def __init__(self, serial_port = '/dev/ttyUSB0', baud_rate = 9600, read_timeout=1):
        self.conn = serial.Serial(serial_port, baud_rate)
        self.conn.timeout = read_timeout
        print("Arduino инициализирована")
    def Set_Pin_Mode(self, pin_number, mode):
        command = (''.join(('M',mode,str(pin_number)))).encode()
        self.conn.write(command)
    def Digital_Read(self, pin_number):
        command = (''.join(('RD', str(pin_number)))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':')
        if header == ('D'+ str(pin_number)):
            return int(value)
    def Digital_Write(self, pin_number, digital_value):
        command = (''.join(('WD', str(pin_number), ':', str(digital_value)))).encode()
        self.conn.write(command)
    def Analog_Read(self, pin_number):
        command = (''.join(('RA', str(pin_number)))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value = line_received.split(':')
        if header == ('A'+ str(pin_number)):
            return int(value)
    def Analog_Write(self, pin_number, analog_value):
        command = (''.join(('WA', str(pin_number), ':', str(analog_value)))).encode()
        self.conn.write(command)
    def DHT_Read(self):
        command = (''.join(('S'))).encode()
        self.conn.write(command)
        line_received = self.conn.readline().decode().strip()
        header, value_h, value_t = line_received.split(':')
        if header == ('S'):
            return (value_h, value_t)
    def Close(self):
        self.conn.close()
        print ("Соединение с Arduino закрыто")


class S7300():
    def __init__(self, ip_addr = '192.168.1.111',  rack = 0, slot = 2):
        self.plc = snap7.client.Client()
        self.plc.connect(ip_addr, rack, slot)
        if self.plc.get_connected():
            print('S7-300 инициализирован')
        else:
            print('Нет связи с S7-300')

    """
    Area table
    Value Mean
    S7AreaPE 0x81 Process Inputs.  - areas['PE']
    S7AreaPA 0x82 Process Outputs. - areas['PA']
    S7AreaMK 0x83 Merkers.         - areas['MK']
    S7AreaDB 0x84 DB               - areas['DB']
    S7AreaCT 0x1C Counters.        - areas['CT']
    S7AreaTM 0x1D Timers           - areas['TM']
    """

    def Write_DOutput( self,bytebit,cmd):
        byte,bit = bytebit.split('.')
        byte,bit = int(byte),int(bit)
        data = self.plc.read_area(areas['PA'],0,byte,1)
        set_bool(data,0,bit,cmd)
        self.plc.write_area(areas['PA'],0,byte,data)

    def Read_DOutput(self,bytebit):
        byte,bit = bytebit.split('.')
        byte,bit = int(byte),int(bit)
        data = self.plc.read_area(areas['PA'],0,byte,1)
        status = get_bool(data,0,bit)
        return status

    def Write_Merker(self,bytebit,cmd):
        byte,bit = bytebit.split('.')
        byte,bit = int(byte),int(bit)
        data = self.plc.read_area(areas['MK'],0,byte,1)
        set_bool(data,0,bit,cmd)
        self.plc.write_area(areas['MK'],0,byte,data)

    def Read_Merker(self,bytebit):
        byte,bit = bytebit.split('.')
        byte,bit = int(byte),int(bit)
        data = self.plc.read_area(areas['MK'],0,byte,1)
        status = get_bool(data,0,bit)
        return status

    def ReadDB(self,dbnum, bytebit, length):
        byte,bit = bytebit.split('.')
        byte,bit = int(byte),int(bit)
        data = self.plc.read_area(areas['DB'],dbnum, byte, length)
        value = round(get_real(data,0)*100)/100
        return value

    def Close(self):
        self.plc.disconnect()
        print ("Соединение с Siemens S7-300 закрыто")
