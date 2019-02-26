from scapy.all import *

def printinfo(pkt):
    if IP in pkt:
        print("Source IP: " + str(pkt[IP].src) + " " + "Destination IP: " + str(pkt[IP].dst) + " ")
    if TCP in pkt:
        print("Source Port: " + str(pkt[TCP].sport) + " " + "Destination Port: " + str(pkt[TCP].dport) + "Protocol: [TCP]")
    if UDP in pkt:
        print("Source Port: " + str(pkt[UDP].sport) + " " + "Destination Port: " + str(pkt[UDP].dport) + "Protocol: [UDP]")

# check if the arguments are filled in
if len(sys.argv) != 2:
    print("There are missing arguments. Usage: Python3 %s <network interface>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])
# interval = str(sys.argv[2])
# collector = str(sys.argv[3])

sniff(iface=interface,filter="ip and tcp or udp",prn=printinfo)