from pymongo import MongoClient

# test code
client = MongoClient('mongodb://localhost:27017/')
db = client["package"]
col = db["packetinfo"]
data = [{
    'ipSrc': '',
    'ipDst': '',
    'sPort': '',
    'dPort': '',
    'proto': '',
    'countTcp': '',
    'countUdp': '',
    'utcTime': ''
}]
col.insert(data)

dblist = client.list_database_names()
print(client.list_database_names())
if db in dblist:
    print("Database already exists.")