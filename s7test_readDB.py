import snap7.client
from snap7.snap7types import *
from snap7.util import *


class DBObject(object):
    pass

offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":6,"String":256}

db=\
"""
Temp_in_room Real 0.0
Temp_in_outdoor Real 4.0
temp2 Real 8.0
"""

def DBRead(plc,db_num,length,dbitems):
    data = plc.read_area(areas['DB'],db_num,0,length)
    obj = DBObject()
    for item in dbitems:
        value = None
        offset = int(item['bytebit'].split('.')[0])

        if item['datatype']=='Real':
            value = get_real(data,offset)

        if item['datatype']=='Bool':
            bit =int(item['bytebit'].split('.')[1])
            value = get_bool(data,offset,bit)

        if item['datatype']=='Int':
            value = get_int(data, offset)

        if item['datatype']=='String':
            value = get_string(data, offset)

        obj.__setattr__(item['name'], value)
    return obj

def get_db_size(array,bytekey,datatypekey):
    seq,length = [x[bytekey] for x in array],[x[datatypekey] for x in array]
    idx = seq.index(max(seq))
    lastByte = int(max(seq).split('.')[0])+(offsets[length[idx]])
    return lastByte

if __name__ == "__main__":
    plc = snap7.client.Client()
    plc.connect('192.168.0.111',0,2)
    itemlist = list(filter(lambda a: a!='',db.split('\n')))

#    for i in range(len(itemlist)):
#       print(itemlist[i])
#    items = [{"name":x,"datatype":x,"bytebit":x} for x in itemlist]

    items = [
        {
            "name": 'Temp_in_room',
            "datatype": 'Real',
            "bytebit": '0.0'
        },
        {
            "name": 'Temp_in_outdoor',
            "datatype": 'Real',
            "bytebit": '4.0'
        },
        {
            "name": 'temp2',
            "datatype": 'Real',
            "bytebit": '8.0'
        }
        ]

    length = get_db_size(items,'bytebit','datatype')
    meh = DBRead(plc,1,length,items)
    print ("""
    Temp_in_room:\t\t\t{}
    Temp_in_outdoor:\t\t{}
    temp2:\t{}
    """.format(meh.Temp_in_room,meh.Temp_in_outdoor,meh.temp2))
    plc.disconnect();