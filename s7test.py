import snap7.client
from snap7.snap7types import *
from snap7.util import *

plc.

if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.0.111',0,0)
    plc.write_area
    plc.ab_write()
