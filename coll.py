# The collector
from dbconnect import client
from sniff import start_detector

def collect(dbconnect):



def dbwrite():
    try:
        db = client["package"]
        col = db["packetinfo"]
        col.insert = [{
            'ipSrc': ipSrc,
            'ipDst': ipDst,
            'sPort': sPort,
            'dPort': dPort,
            'proto': '', #protocol
            'countTcp': countTCP,
            'bytesTcp': countByteTCP,
            'countUdp': counUDP,
            'bytesUdp': countByteUDP,
            'utcTime': packetTime
        }]
    except Exception as e:
        print(e)
