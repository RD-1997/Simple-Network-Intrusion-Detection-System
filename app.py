from flask import Flask, render_template
from dbconnect import client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yaml

# importing yaml configuration file for that extra security
with open("config.yaml", "r") as ymlfile:
    cfg = yaml.load(ymlfile)

# defining the mongodb values
db = client[cfg['mongodb']['db']]
col = db[cfg['mongodb']['collection']]
package = client.package

# creating empty dataframe
dFrame = pd.DataFrame()

# looping over the database and retrieving all values
for obj in col.find():

    # retrieving the following values and store them in variables
    detector = obj['detector']
    starttime = obj['startTime']
    starttime = datetime.utcfromtimestamp(float(starttime)).strftime('%Y-%m-%d %H:%M:%S')
    endtime = obj['endTime']
    endtime = datetime.utcfromtimestamp(float(endtime)).strftime('%Y-%m-%d %H:%M:%S')

    # put all values in a new dataframe dynamically
    newDf = pd.DataFrame()
    newDf['signature'] = obj['signature']
    newDf['packets'] = obj['totalpackets']
    newDf['starttime'] = starttime
    newDf['endtime'] = endtime
    newDf['detector'] = detector

    # finally, append the new data frame to the existing one for all results
    dFrame = dFrame.append(newDf)

# segregating the signature to individual columns and values
updatedDf = dFrame["signature"].str.split(":", n=4, expand=True)
dFrame["src_ip"] = updatedDf[0]
dFrame["src_port"] = updatedDf[1]
dFrame["dest_ip"] = updatedDf[2]
dFrame["dest_port"] = updatedDf[3]
dFrame["protocol"] = updatedDf[4]

# update the disected signature as new columns to the existing main data frame
dFrame = dFrame[dFrame['src_ip'].map(len) > 5]
dFrame = dFrame[dFrame['src_port'].map(len) < 6]
dFrame = dFrame[dFrame['dest_ip'].map(len) > 5]
dFrame = dFrame[dFrame['dest_port'].map(len) < 6]

# counting the amount of signatures
sumofsignature = dFrame.shape[0]
print(sumofsignature)

# re arranging the columns and leaving out the signature column
dFrame = dFrame[['src_ip', 'src_port', 'dest_ip', 'dest_port', 'protocol', 'packets', 'starttime', 'endtime', 'detector']]
columns = dFrame.columns

############################################## START BAR CHART ########################################################################

# preparing dataset for bar chart
dFrame.packets = dFrame.packets.astype(int)

# creating new dataframe for the barchart
lawlDf = pd.DataFrame()
lawlDf = dFrame[['starttime', 'packets']]
lawlDf = lawlDf.groupby('starttime', as_index=False).agg(sum)
totalsniffs = lawlDf.shape[0]
print(totalsniffs)

# total packets
sumofpackets = dFrame['packets'].sum()
print(sumofpackets)

# columns to use for bar chart
packets = lawlDf['packets']
sniffDate = lawlDf['starttime']

# creating the bar chart
plt.barh(sniffDate, packets, .8)
axes = plt.gca()
plt.xticks(rotation=60)
plt.yticks(fontsize='8')
plt.ylabel("Interval")
plt.xlabel("Total packets")
plt.title("Total sniffed packets per interval")

# saving the bar chart
plt.savefig('static/images/ipchart.png', bbox_inches='tight')
plt.show()
############################################## END BAR CHART ########################################################################

############################################## START PIE CHART ########################################################################

# preparing the data set for the piechart to use
lolFrame = pd.DataFrame()

# using the relevant columns and put them in a new data frame
lolFrame = dFrame[['packets', 'protocol']]

# Aggregating the total packets per protocol
lolFrame = lolFrame.groupby('protocol', as_index=False).agg(sum)

#some bs color scheme for the piechart
colors = ["#E13F29", "#D69A80", "#D63B59", "#AE5552", "#CB5C3B", "#EB8076", "#96624E"]

# Create a pie chart
plt.pie(
    lolFrame['packets'],
    labels=lolFrame['protocol'],
    shadow=True,
    colors=colors,
    explode=(0, 0.1),
    startangle=90,
    autopct='%1.1f%%',
    )

# View the plot drop above
plt.axis('equal')
plt.title("Protocol sniffed")

# View the plot
plt.tight_layout()

# saving the plot as an image
plt.savefig('static/images/piechart.png', bbox_inches='tight')
plt.show()

############################################ END PIE CHART ############################################################################


# defining the flask app
app = Flask(__name__)

@app.route("/")
def web():
    return render_template('dashboard_v3.html', data=dFrame, columns=columns, totalpkt=sumofpackets, totalroute=sumofsignature, totalsniffs=totalsniffs)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')