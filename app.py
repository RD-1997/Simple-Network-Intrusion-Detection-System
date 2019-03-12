from flask import Flask, render_template
from dbconnect import client
from sniff import tcpPacket, udpPacket

app = Flask(__name__)

# open connection
package = client.package

@app.route("/")
def web():
    udpList = udpPacket
    tcpList = tcpPacket
    return render_template('index.html', udpList=udpList, tcpList=tcpList)

if __name__ == '__main__':
    app.run()
