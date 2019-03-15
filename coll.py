# The collector
import json
from dbconnect import client


class manageTraffic():
    def __init__(self, detector):
        self.detector = detector

    def structureTraffic(self, signature, totalPackets, totalBytes, startTime, packetTime):

        db = client["package"]
        col = db["packetinfo"]

        data = [{
            'general': [
                {
                    'detector': self.detector,
                    'startTime': startTime,
                    'endTime': packetTime
                }],
            'sniffInfo': [
                {
                    'traffic': signature,
                    'totalPackets': totalPackets,
                    'totalBytes': totalBytes
                }]
        }]

        json.dumps(data)

        print(json.dumps(data, indent=2))
        col.insert(data)



