#!/usr/bin/python
from collections import Counter
from scapy.all import *
import time
from threading import Thread
from coll import manageTraffic


if len(sys.argv) != 3:
    print("There are missing arguments. Usage: Python3 %s <network interface> <interval in minutes>" % (sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])  # user specifies the network interface
interval = str(sys.argv[2])  # user specifies the interval time
intervalInt = float(interval) * 60  # converts the minutes given by the user into seconds and creates an integer
# collector = str(sys.argv[3])

packetTime = str(time.time())  # variable to determine packet time in UTC format

# Create a Packet Counter
packet_counts = Counter()

def printinfo(packet):
    global startTime
    try:

        startTime = str(time.time())

        if TCP in packet:
            proto = "TCP"
            key = tuple(sorted([packet[0][1].src, str(packet[0][1].sport), packet[0][1].dst, str(packet[0][1].dport), proto]))
            packet_counts.update([key])
            print(f"Packet #{sum(packet_counts.values())}: {packet[0][1].src}:{packet[0][1].sport} => {packet[0][1].dst}:{packet[0][1].dport} | {proto}")

        if UDP in packet:
            proto = "UDP"
            key = tuple(sorted([packet[0][1].src, str(packet[0][1].sport), packet[0][1].dst, str(packet[0][1].dport), proto]))
            packet_counts.update([key])
            print(f"Packet #{sum(packet_counts.values())}: {packet[0][1].src}:{packet[0][1].sport} => {packet[0][1].dst}:{packet[0][1].dport} | {proto}")

    except Exception as e:
        print(e)


# the actual sniffer
def sniffThatSh():
    global packet_counts
    print("[*] Start sniffing...\n")
    sniff(iface=interface, filter="ip and tcp or udp", prn=printinfo, timeout=intervalInt)
    print("[*] Stop sniffing\n")

    signatureList = []
    packetList = []

    for key, count in packet_counts.items():
        if str(key[4]) == "TCP":
            signature = str(key[0]) + ":" + str(key[2]) + ":" + str(key[1]) + ":" + str(key[3]) + ":" + str(key[4])
            signatureList.append(signature)
            totalpackets = str(count)
            packetList.append(totalpackets)

        if str(key[4]) == "UDP":
            signature = str(key[0]) + ":" + str(key[2]) + ":" + str(key[1]) + ":" + str(key[3]) + ":" + str(key[4])
            signatureList.append(signature)
            totalpackets = str(count)
            packetList.append(totalpackets)

    # parsing the information to the class so it can be stored in the database
    detector = manageTraffic("detector1")
    detector.structureTraffic(signatureList, packetList, startTime, packetTime)
    packet_counts = Counter()
    time.sleep(5)  # sleeps for 5 seconds

    sniffThatSh()       # repeats the code


Thread(target=sniffThatSh).start()  # executing the code

