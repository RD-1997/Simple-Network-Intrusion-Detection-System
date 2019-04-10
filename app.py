from flask import Flask, render_template
from dbconnect import client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yaml

with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

db = client[cfg['mongodb']['db']]
col = db[cfg['mongodb']['collection']]
package = client.package

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
    newDf['endtime'] = endtime
    newDf['detector'] = detector

    dFrame = dFrame.append(newDf)


updatedDf = dFrame["signature"].str.split(":", n=4, expand=True)
dFrame["src_ip"] = updatedDf[0]
dFrame["src_port"] = updatedDf[1]
dFrame["dest_ip"] = updatedDf[2]
dFrame["dest_port"] = updatedDf[3]
dFrame["protocol"] = updatedDf[4]

dFrame = dFrame[dFrame['src_ip'].map(len) > 5]
dFrame = dFrame[dFrame['src_port'].map(len) < 6]
dFrame = dFrame[dFrame['dest_ip'].map(len) > 5]
dFrame = dFrame[dFrame['dest_port'].map(len) < 6]


sumofsignature = dFrame.shape[0]
print(sumofsignature)

dFrame = dFrame[['src_ip', 'src_port', 'dest_ip', 'dest_port', 'protocol', 'packets', 'starttime', 'endtime', 'detector']]
columns = dFrame.columns

#print(dFrame.to_string())

dFrame.packets = dFrame.packets.astype(int)
dFrame = dFrame.sort_values(by=['packets'])

sumofpackets = dFrame['packets'].sum()
print(sumofpackets)

packets = dFrame['packets']
sniffDate = dFrame['starttime']

plt.barh(sniffDate, packets, .8)
axes = plt.gca()
plt.xticks(rotation=60)
plt.yticks(fontsize='8')
plt.ylabel("Interval")
plt.xlabel("Total packets")
plt.title("Total sniffed packets per interval")
plt.savefig('static/images/ipchart.png', bbox_inches='tight')
plt.show()

# dataset for the piechart to use
lolFrame = pd.DataFrame()
lolFrame = dFrame[['packets', 'protocol']]
lolFrame = lolFrame.groupby('protocol', as_index=False).agg(sum)
print(list(lolFrame))
colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]

# Create a pie chart
plt.pie(
    # using data total)arrests
    lolFrame['packets'],
    # with the labels being officer names
    labels=lolFrame['protocol'],
    # with no shadows
    shadow=False,
    # with colors
    colors=colors,
    # with one slide exploded out
    explode=(0, 0.1),
    # with the start angle at 90%
    startangle=90,
    # with the percent listed as a fraction
    autopct='%1.1f%%',
    )

# View the plot drop above
plt.axis('equal')
plt.title("Protocol sniffed")

# View the plot
plt.tight_layout()
plt.savefig('static/images/piechart.png', bbox_inches='tight')
plt.show()

app = Flask(__name__)

@app.route("/")
def web():
    return render_template('dashboard_v3.html', data=dFrame, columns=columns, totalpkt=sumofpackets, totalroute=sumofsignature)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')