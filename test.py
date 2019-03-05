from scapy.all import *

def printinfo(pkt):
    if IP in pkt:
        print(pkt.sprintf("%IP.len%"))


sniff(iface="ens33",filter="ip",prn=printinfo)