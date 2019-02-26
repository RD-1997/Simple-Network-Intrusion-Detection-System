import logging 
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys 
from scapy.all import *
from datetime import datetime

# creating the class
class ids: 
    
    # Defining the tcp flags
    __flags = {
        'F': 'FIN',
        'S': 'SYN',
        'R': 'RST',
        'P': 'PSH',
        'A': 'ACK',
        'U': 'URG',
        'E': 'ECE',
        'C': 'CWR',
        }


    # function to scan packets over wifi
    def sniffPackets(self,packet):

        cache = []
        # scanning IP packets
        if packet.haslayer(IP):
            pckt_src=packet[IP].src
            pckt_dst=packet[IP].dst
            print("Packet: SRC: %s  ==>  DST: %s  , TIME: %s"%(pckt_src,pckt_dst,str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))), end=' ')
            cache.append(packet)

        # capturing TCP traffic
        if packet.haslayer(TCP):
            src_port=packet.sport
            dst_port=packet.dport
            print(", Protocol: [TCP], Port: %s --> %s, "%(src_port,dst_port), end='')
            print([type(self).__flags[x] for x in packet.sprintf('%TCP.flags%')])
            cache.append(packet)

        # capturing UDP traffic
        if packet.haslayer(UDP):
            src_port=packet.sport
            dst_port=packet.dport
            print(", Protocol: [UDP], Port: %s --> %s, "%(src_port, dst_port), end='')
            print("")
            print("")
            cache.append(packet)

        else:
            print()

# ######################### Logics #############################################################

# check if the arguments are filled in
if len(sys.argv) != 2:
    print("There are missing arguments. Usage: Python3 %s <network interface>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])
# interval = str(sys.argv[2])
# collector = str(sys.argv[3])



# asks for an extra confirmation to run the code
answer = str(input("Are you sure you want to continue? (y/n): ")).lower()

if answer.startswith('y'):
    packetList = []
    print("Network Intrusion Detection System ")
    packetList = sniff(filter="ip",iface=interface,prn=ids().sniffPackets,store=1)
    print(packetList)
    packetList.nsummary()


elif answer.startswith('n'):
    print("Operation aborted.")

else:
    print("Please give a valid answer. Thank you.")


