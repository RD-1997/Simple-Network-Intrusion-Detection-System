# The collector
import json
from dbconnect import client
import socket
import pickle


class manageTraffic():
    def __init__(self, detector):
        self.detector = detector

    def structureTraffic(self, signature, totalpackets, startTime, packetTime):

        #data will be sent to server over socket
        HOST = '127.0.0.1'
        PORT = 50011

        db = client["package"]
        col = db["packetinfo"]

        data = {

             "detector": self.detector,
             "startTime": startTime,
             "endTime": packetTime,
             "signature": signature,
             "totalpackets": totalpackets
         }

        # Create a socket connection.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))

        # Pickle the object and send it to the server
        data_string = pickle.dumps(data)
        s.send(data_string)

        s.close()
        print('Data Sent to Server')





