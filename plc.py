from snap7.util import *
from snap7.snap7types import *

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

def WriteOutput(dev,bytebit,cmd):
    byte,bit = bytebit.split('.')
    byte,bit = int(byte),int(bit)
    data = dev.read_area(areas['PA'],0,byte,1)
    set_bool(data,0,bit,cmd)
    dev.write_area(0x82,0,byte,data)

def ReadOutput(dev,bytebit):
    byte,bit = bytebit.split('.')
    byte,bit = int(byte),int(bit)
    data = dev.read_area(areas['PA'],0,byte,1)
    status = get_bool(data,0,bit)
    return status

def WriteMerker(dev,bytebit,cmd):
    byte,bit = bytebit.split('.')
    byte,bit = int(byte),int(bit)
    data = dev.read_area(areas['MK'],0,byte,1)
    set_bool(data,0,bit,cmd)
    dev.write_area(0x83,0,byte,data)

def ReadMerker(dev,bytebit):
    byte,bit = bytebit.split('.')
    byte,bit = int(byte),int(bit)
    data = dev.read_area(areas['MK'],0,byte,1)
    status = get_bool(data,0,bit)
    return status
