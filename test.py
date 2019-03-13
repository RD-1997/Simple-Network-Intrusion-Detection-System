from pymongo import MongoClient

# test code
client = MongoClient('mongodb://localhost:27017/')
db = client["package"]
col = db["packetinfo"]
data = [{
    'ipSrc': '1',
    'ipDst': '2',
    'sPort': '3',
    'dPort': '4',
    'proto': '5',
    'countTcp': '6',
    'countUdp': '7',
    'utcTime': '8'
}]
col.insert(data)

dblist = client.list_database_names()
print(client.list_database_names())
if db in dblist:
    print("Database already exists.")




# ###
# '''
# 'ipSrc': '',
# 'ipDst': '',
# 'sPort': '',
# 'dPort': '',
# 'protoTcp': '',
# 'protoUdp': '',
# 'countTcp': '',
# 'bytesTcp': '',
# 'countUdp': '',
# 'bytesUdp': '',
# 'utcTime': ''
# '''
#
# def start_detector(pkt):
# # Collect data
#     global countTCP, countUDP
#
#     if IP in pkt:
#         ipSrc = pkt[IP].src
#         ipDst = pkt[IP].dst
#         sPort = pkt[IP].sport
#         dPort = pkt[IP].dport
#
#         print(str(ipSrc) + ":" + str(sPort) + " --> " + str(ipDst) + ":" + str(dPort) + " | ", end='')
#         print("")
#     if TCP in pkt:
#         countTCP +=1
#         protoTcp = "TCP"
#         print(protoTcp + " | " + " UTC Timestamp: " + packetTime + " | TCP Packet number: " + str(countTCP), end='')
#         print("")
#
#     if UDP in pkt:
#         countUDP +=1
#         protoUdp = "UDP"
#         print(protoUdp + " | "  + " UTC Timestamp: " + packetTime + " | UDP Packet number: " + str(countUDP), end='')
#         print("")