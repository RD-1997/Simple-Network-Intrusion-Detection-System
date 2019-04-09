from flask import Flask, render_template
from dbconnect import client
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

db = client["package"]
col = db["packetinfo"]

dFrame = pd.DataFrame()

for obj in col.find():

    detector = obj['detector']
    starttime = obj['startTime']
    starttime = datetime.utcfromtimestamp(float(starttime)).strftime('%Y-%m-%d %H:%M:%S')
    endtime = obj['endTime']
    endtime = datetime.utcfromtimestamp(float(endtime)).strftime('%Y-%m-%d %H:%M:%S')
    newDf = pd.DataFrame()
    newDf['signature'] = obj['signature']
    newDf['packets'] = obj['totalpackets']
    newDf['starttime'] = starttime
    newDf['endTime'] = endtime
    newDf['detector'] = detector

dFrame = dFrame.append(newDf)


dFrame.packets = dFrame.packets.astype(int)
dFrame = dFrame.sort_values(by=['packets'])
#print(dFrame.to_string())

packets = dFrame['packets'][100:130]
ips = dFrame['signature'][100:130]

plt.barh(ips, packets, .8)
axes = plt.gca()
axes.set_xlim([1, 100])
plt.xticks(rotation='vertical')
plt.yticks(fontsize='8')
plt.ylabel("IP Addresses")
plt.xlabel("Packet count")
plt.title("bar chart")
plt.savefig('static/images/ipchart.png', bbox_inches='tight')
#plt.show()

app = Flask(__name__)


sumofpackets = dFrame['packets'].sum()
print(sumofpackets)

sumofsignature = dFrame.shape[0]
print(sumofsignature)

# open connection
package = client.package

@app.route("/")
def web():
    return render_template('dashboard_v3.html', tables=[dFrame.to_html(classes='data')], titles=dFrame.columns.values, totalpkt=sumofpackets, totalroute=sumofsignature)

if __name__ == '__main__':
    app.run()