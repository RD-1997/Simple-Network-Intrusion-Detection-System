from scapy.all import *

def printinfo(pkt):
    if IP in pkt:
        print("Source IP: " + str(pkt[IP].src) + " " + "Destination IP: " + str(pkt[IP].dst) + " ")
    if TCP in pkt:
        print("Source Port: " + str(pkt[TCP].sport) + " " + "Destination Port: " + str(pkt[TCP].dport) + "Protocol: [TCP]")
    if UDP in pkt:
        print("Source Port: " + str(pkt[UDP].sport) + " " + "Destination Port: " + str(pkt[UDP].dport) + "Protocol: [UDP]")

sniff(iface="ens33",filter="ip and tcp or udp",prn=printinfo)