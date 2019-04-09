import socket, pickle, json, threading
from dbconnect import client
import yaml

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

HOST = cfg['socket']['ip']
PORT = cfg['socket']['port']

db = client[cfg['mongodb']['db']]
col = db[cfg['mongodb']['collection']]

print("Creating socket...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket succesfully created")
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Trying to bind...")
s.bind((HOST, PORT))
print("Succesfully bound to, ", (HOST, PORT))
s.listen(1)
print("Listening for connection...")

while True:
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(8192)
    if not data: break
    data_variable = pickle.loads(data)
    conn.close()
   # print(data_variable)

    newjson = json.dumps(data_variable)
    # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
    #print(newjson)

    print('Data received from client and inserted in db')
    db = client[cfg['mongodb']['db']]
    col = db[cfg['mongodb']['collection']]
    col.insert(data_variable)



