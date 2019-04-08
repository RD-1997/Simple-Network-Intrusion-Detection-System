from scapy.all import *
import time
from threading import Thread
from coll import manageTraffic


# check if the arguments are filled in
if len(sys.argv) != 3:
    print("There are missing arguments. Usage: Python3 %s <network interface> <interval in minutes>" % (sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])  # user specifies the network interface
interval = str(sys.argv[2])  # user specifies the interval time
intervalInt = int(interval) * 60  # converts the minutes given by the user into seconds and creates an integer
# collector = str(sys.argv[3])

# widely used variables
countTCP = 0
countUDP = 0
bytePerPackageTCP = 0
bytePerPackageUDP = 0
totalByteTCP = 0
totalByteUDP = 0
packetTime = str(time.time())  # variable to determine packet time in UTC format
taskID = 0  # variable to determine each task
signatureList = []


# function for the scan details
def printinfo(pkt):
    global countTCP, countUDP, totalByteTCP, totalByteUDP, bytePerPackageTCP, bytePerPackageUDP, startTime
    try:

        startTime = str(time.time())

        if IP in pkt:
            ipSrc = pkt[IP].src
            ipDst = pkt[IP].dst
            sPort = pkt[IP].sport
            dPort = pkt[IP].dport

        if TCP in pkt:
            countTCP += 1
            proto = "TCP"
            totalByteTCP += int(pkt.sprintf("%IP.len%"))
            bytePerPackageTCP = int(pkt.sprintf("%IP.len%"))

            signature = str(ipSrc) + ":" + str(sPort) + ":" + str(ipDst) + ":" + str(dPort) + ":" + str(proto)

            if signature not in signatureList:
                signatureList.append(signature)


        if UDP in pkt:
            countUDP += 1
            proto = "UDP"
            totalByteUDP += int(pkt.sprintf("%IP.len%"))
            bytePerPackageUDP = int(pkt.sprintf("%IP.len%"))

            signature = str(ipSrc) + ":" + str(sPort) + ":" + str(ipDst) + ":" + str(dPort) + ":" + str(proto)

            if signature not in signatureList:
                signatureList.append(signature)


    except Exception as e:
        print(e)


# function to activate the scanner
def sniffThatSh():
    global countTCP, countUDP, taskID
    packetList = []  # creates a list where the scan results can be saved
    print("[*] Start sniffing...\n")
    packetList = sniff(iface=interface, filter="ip and tcp or udp", prn=printinfo, timeout=intervalInt)
    print("[*] Stop sniffing\n")

    #parsing the information to the class so it can be stored in the database
    detector = manageTraffic("detector1")
    totalPackets = str(countUDP + countTCP)
    totalBytes = str(totalByteUDP + totalByteTCP)

    detector.structureTraffic(signatureList, totalPackets, totalBytes, startTime, packetTime)

    time.sleep(5)  # sleeps for 5 seconds

    countTCP = 0
    countUDP = 0
    # sniffThatSh()       # repeats the code


Thread(target=sniffThatSh).start()  # executing the code