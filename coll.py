# The collector
import socket
import pickle
import yaml

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)


class manageTraffic():
    def __init__(self, detector):
        self.detector = detector

    def structureTraffic(self, signature, totalpackets, startTime, packetTime):

        #data will be sent to server over socket
        HOST = cfg['socket']['ip']
        PORT = cfg['socket']['port']

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
        print('Data sent to collector')





