from scapy.all import *
import json
import time
from threading import Thread
from dbconnect import client
from coll import manageTraffic

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
countTCP = 0
countUDP = 0
bytePerPackageTCP = 0
bytePerPackageUDP = 0
totalByteTCP = 0
totalByteUDP = 0
# tcpPacket = []
# udpPacket = []
packetTime = str(time.time())       # variable to determine packet time in UTC format
taskID = 0                          # variable to determine each task





srcList = []
dstList = []
sPortList = []
dPortList = []






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

            if ipSrc not in srcList:
                srcList.append(ipSrc)

            if ipDst not in dstList:
                dstList.append(ipDst)

            if sPort not in sPortList:
                sPortList.append(sPort)

            if dPort not in dPortList:
                dPortList.append(dPort)


        if TCP in pkt:
            countTCP +=1
            totalTraffic = str(countTCP)
            proto = "TCP"
            totalByteTCP += int(pkt.sprintf("%IP.len%"))
            totalBytes = str(totalByteTCP)
            bytePerPackageTCP = int(pkt.sprintf("%IP.len%"))
            bytePerPackage = str(bytePerPackageTCP)

            detector = manageTraffic("detector1")
            detector.structureTraffic(srcList, dstList, sPortList, dPortList, proto, totalTraffic, totalBytes, bytePerPackage, packetTime)

        if UDP in pkt:
            countUDP +=1
            totalTraffic = str(countUDP)
            proto = "UDP"
            totalByteUDP += int(pkt.sprintf("%IP.len%"))
            totalBytes = str(totalByteUDP)
            bytePerPackageUDP = int(pkt.sprintf("%IP.len%"))
            bytePerPackage = str(bytePerPackageUDP)

            detector = manageTraffic("detector1")
            detector.structureTraffic(ipSrc, ipDst, sPort, dPort, proto, totalTraffic, totalBytes, bytePerPackage, packetTime)

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
    countTCP = 0
    countUDP = 0
    taskID += 1


    print("Your Task ID is: " + str(taskID) + " Sending information to collector....\n")


    time.sleep(5)       # sleeps for 5 seconds

    #sniffThatSh()       # repeats the code


Thread(target=sniffThatSh).start()           # executing the code