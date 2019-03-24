import snap7
import plc as PLC

myplc = snap7.client.Client()
myplc.connect('192.168.0.111',0,2)
print(myplc.get_connected())
t = '10.0'
PLC.WriteMerker(myplc,t, 0)
myplc.disconnect()

