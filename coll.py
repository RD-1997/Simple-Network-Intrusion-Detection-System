# The collector
import socket
import pickle
import yaml
import ssl, traceback, sys

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# socket variables
HOST = cfg['socket']['ip']
PORT = cfg['socket']['port']

# secure socket variables
ssl_version = ssl.PROTOCOL_SSLv23
certfile = cfg['ssl']['certificate']
keyfile = cfg['ssl']['key']

option_test_switch = 1  # to test, change to 1

if option_test_switch == 1:
    print("ver=", ssl_version, "certfile=", certfile, "keyfile=", \
    keyfile, "HOST=", HOST, "PORT=", PORT)

def ssl_wrap_socket(sock, ssl_version=None, keyfile=None, certfile=None):
    try:
        sslContext = ssl.SSLContext(ssl_version)
        if option_test_switch == 1:
            print("ssl_version loaded!! =", ssl_version)

        # 3. set root certificate path
        if certfile is not None and keyfile is not None:
            # if specified, load speficied certificate file and private key file
            sslContext.verify_mode = ssl.CERT_REQUIRED
            sslContext.load_verify_locations(certfile, keyfile)
            if option_test_switch == 1:
                print("ssl loaded!! certfile=", certfile, "keyfile=", keyfile)
            return sslContext.wrap_socket(sock)
        else:
            # default certs
            sslContext.verify_mode = ssl.CERT_NONE
            sslContext.load_default_certs()
            return sslContext.wrap_socket(sock)

    except ssl.SSLError:
        print("wrap socket failed!")
        print(traceback.format_exc())
        sock.close()
        sys.exit(-1)


class manageTraffic():
    def __init__(self, detector):
        self.detector = detector

    def structureTraffic(self, signature, totalpackets, startTime, packetTime):
        global HOST, PORT
        # data will be sent to server over socket

        data = {

             "detector": self.detector,
             "startTime": startTime,
             "endTime": packetTime,
             "signature": signature,
             "totalpackets": totalpackets
         }

        # Create a socket connection.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sslSocket = ssl_wrap_socket(s, ssl_version, keyfile, certfile)
        sslSocket.connect((HOST, PORT))

        # Pickle the object and send it to the server
        data_string = pickle.dumps(data)

        sslSocket.send(data_string)

        sslSocket.close()
        print('Data sent to collector')





