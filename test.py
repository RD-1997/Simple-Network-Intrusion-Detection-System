from flask import Flask, render_template
from dbconnect import client
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import yaml

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

############################################### START DATATABLE ########################################################################

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

# segregating starttime to date and time
updatedDf1 = dFrame["starttime"].str.split(" ", n=1, expand=True)
dFrame["date"] = updatedDf1[0]
dFrame["time"] = updatedDf1[1]

print(dFrame.to_string())
