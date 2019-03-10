from bson import json_util
from pymongo import MongoClient
import json

### Steps for test ###
# Test connection
# make a sample data in JSON
# put data into MongoDB
# Take data from MongoDB

# test connection of database
try:
    client = MongoClient('mongodb://localhost:27017/')
    client.server_info()
except pymongo.errors.ConnectionFailure as err:
    print(err)

# try json
file = open('test.txt', 'w')
file.write("Hello1")
file.close()