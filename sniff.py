from scapy.all import *
import json
import time
from threading import Thread
from dbconnect import client

# check if the arguments are filled in
if len(sys.argv) != 3:
    print("There are missing arguments. Usage: Python3 %s <network interface> <interval in minutes>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])        # user specifies the network interface
interval = str(sys.argv[2])         # user specifies the interval time
intervalInt = int(interval) * 60    # converts the minutes given by the user into seconds and creates an integer
# collector = str(sys.argv[3])

# widely used variables
countTCP = 0                        # variable to count the TCP packets
countUDP = 0                        # variable to count the UDP packets
bytePerPackageTCP = 0                  # variable to count each package
bytePerPackageUDP = 0                  # variable to count each package
totalByteTCP = 0                    # variable to count UDP packet sizes in bytes
totalByteUDP = 0                    # variable to count TCP packet sizes in bytes
# tcpPacket = []
# udpPacket = []
packetTime = str(time.time())       # variable to determine packet time in UTC format
taskID = 0                          # variable to determine each task

# function for the scan details
def printinfo(pkt):
    global countTCP, countUDP, totalByteTCP, totalByteUDP, bytePerPackageTCP, bytePerPackageUDP
    try:
        db = client["package"]
        col = db["packetinfo"]
        if IP in pkt:
            ipSrc = pkt[IP].src
            ipDst = pkt[IP].dst
            sPort = pkt[IP].sport
            dPort = pkt[IP].dport
        for TCP in pkt:
            countTCP +=1
            protoTCP = "TCP"
            totalByteTCP += int(pkt.sprintf("%IP.len%"))
            bytePerPackageTCP = int(pkt.sprintf("%IP.len%"))
            data = [{
                'ipSrc': ipSrc,
                'ipDst': ipDst,
                'sPort': sPort,
                'dPort': dPort,
                'proto': protoTCP,
                'countTcp': countTCP,
                'bytesTcp': totalByteTCP,
                'bytePerTcp': bytePerPackageTCP,
                'utcTime': packetTime
            }]
            col.insert(data)
        for UDP in pkt:
            countUDP +=1
            protoUDP = "UDP"
            totalByteUDP = int(pkt.sprintf("%IP.len%"))
            bytePerPackageUDP = int(pkt.sprintf("%IP.len%"))
            data = [{
                'ipSrc': ipSrc,
                'ipDst': ipDst,
                'sPort': sPort,
                'dPort': dPort,
                'proto': protoUDP,
                'countUdp': countUDP,
                'bytesUdp': totalByteUDP,
                'bytePerTcp': bytePerPackageUDP,
                'utcTime': packetTime
            }]
            col.insert(data)
    except Exception as e:
        print(e)


# function to activate the scanner
def sniffThatSh():
    packetList = []     # creates a list where the scan results can be saved
    print("[*] Start sniffing...\n")
    packetList = sniff(iface=interface,filter="ip and tcp or udp",prn=printinfo, timeout=intervalInt)
    print("[*] Stop sniffing\n")

    global countTCP
    global countUDP
    global taskID
    countTCP = 0        # resets the TCP count
    countUDP = 0        # resets the UDP count
    taskID += 1         # classify each task by tasknumber.

    print("Your Task ID is: " + str(taskID) + " Sending information to collector....\n")
    #print(packetList)   # shows list details
    # for f in tcpPacket:
    #     print(f)
    #
    # for x in udpPacket:
    #     print(x)

    time.sleep(5)       # sleeps for 5 seconds

    #sniffThatSh()       # repeats the code


Thread(target=sniffThatSh).start()           # executing the code