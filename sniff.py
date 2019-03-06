from scapy.all import *
import json
import time


# check if the arguments are filled in

if len(sys.argv) != 3:

    print("There are missing arguments. Usage: Python3 %s <network interface>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments

interface = str(sys.argv[1]) # user specifies the network interface
interval = str(sys.argv[2])  # user specifies the interval time
intervalInt = int(interval) * 60  # converts the minutes given by the user into seconds
# collector = str(sys.argv[3])


# widely used variables

countTCP = 0
countUDP = 0
countByte = 0
packetTime = str(time.time())

# function for the scan details
def printinfo(pkt):

    global countTCP, countUDP

    if IP in pkt:
        print(str(pkt[IP].src) + ":" + str(pkt[IP].sport) + " --> " + str(pkt[IP].dst) + ":" + str(pkt[IP].dport) + " | ", end='')

    if TCP in pkt:
        countTCP +=1
        print("TCP" + " | " + " UTC Timestamp: " + packetTime + " | TCP Packet number: " + str(countTCP), end='')
        print("")

    if UDP in pkt:
        countUDP +=1
        print("UDP" + " | "  + " UTC Timestamp: " + packetTime + " | UDP Packet number: " + str(countUDP), end='')
        print("")


# function to activate the scanner
def sniffThatSh():

    print("[*] Start sniffing...")
    sniff(iface=interface,filter="ip and tcp or udp",prn=printinfo, timeout=intervalInt)

    print("[*] Stop sniffing")

    print("Sending information to collector....")
    time.sleep(30)

    sniffThatSh()  #repeats the code


sniffThatSh()

