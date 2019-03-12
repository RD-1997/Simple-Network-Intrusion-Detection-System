# The collector
from dbconnect import client
from sniff import start_detector

def collect(dbconnect):



def dbwrite():
    try:
        db = client["package"]
        col = db["packetinfo"]
        col.insert = [{
            'ipSrc': '',amountB
            'ipDst': '',
            'sPort': '',
            'dPort': '',
            'proto': '',
            'countTcp': '',
            'bytesTcp':'',
            'countUdp': '',
            'bytesUdp': '',
            'utcTime': ''
        }]
    except Exception as e:
    Tcp    print(e)