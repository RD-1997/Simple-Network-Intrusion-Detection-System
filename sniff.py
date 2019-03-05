from scapy.all import *

### variables used widely ###
countTCP = 0
countUDP = 0

def printinfo(pkt):
    global countTCP, countUDP
    if IP in pkt:
        print("Source IP: " + str(pkt[IP].src) + " " + "Destination IP: " + str(pkt[IP].dst) +
              " Package in Bytes: " + pkt.sprintf("%IP.len%"))
    if TCP in pkt:
        countTCP +=1
        print("Source Port: " + str(pkt[TCP].sport) + " " + "Destination Port: " +
              str(pkt[TCP].dport) + " Protocol: [TCP]" + " | " + str(countTCP))
    if UDP in pkt:
        countUDP +=1
        print("Source Port: " + str(pkt[UDP].sport) + " " + "Destination Port: " +
              str(pkt[UDP].dport) + " Protocol: [UDP]" + " | " + str(countUDP))

# check if the arguments are filled in
if len(sys.argv) != 2:
    print("There are missing arguments. Usage: Python3 %s <network interface>"%(sys.argv[0]))
    sys.exit(0)

# defining the command line arguments
interface = str(sys.argv[1])
# interval = str(sys.argv[2])
# collector = str(sys.argv[3])


print("[*] Start sniffing...")
sniff(iface=interface,filter="ip and tcp or udp",prn=printinfo,count=10)
print("[*] Stop sniffing")