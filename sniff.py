from scapy.all import *
import json
import time

### widely used variables ###
countTCP = 0
countUDP = 0
countByte = 0
time = str(time.time())

def printinfo(pkt):
    global countTCP, countUDP

    if IP in pkt:
        print(str(pkt[IP].src) + ":" + str(pkt[IP].sport) + " --> " + str(pkt[IP].dst) + ":" + str(pkt[IP].dport) + " | ", end='')

    if TCP in pkt:
        countTCP +=1
        print("TCP" + " | " + str(countTCP) + " UTC Timestamp: " + time , end='')
        print("")

    if UDP in pkt:
        countUDP +=1
        print("UDP" + " | " + str(countUDP) + "UTC Timestamp: " + time , end='')
        print("")

# check if the arguments are filled in
if len(sys.argv) != 2:
    print("There are missing arguments. Usage: Python3 %s <network interface>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])
# interval = str(sys.argv[2])
# collector = str(sys.argv[3])


print("[*] Start sniffing...")
sniff(iface=interface,filter="ip and tcp or udp",prn=printinfo, count=50)
print("[*] Stop sniffing")