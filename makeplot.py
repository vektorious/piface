#!/usr/bin/python
# coding: utf8

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import csv
import datetime
from time import sleep, strftime, time
import os

timepoints = list()

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

filename = "/home/pi/templog_data/flat_parameter_{0}.csv".format(yesterday)
savename = '/home/pi/templog_data/graphs/'+filename.split('/')[-1].split('.')[0] + ".png"

with open(filename) as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['time', 'temp', 'humidity'])
    for row in reader:
        timepoints.append(datetime.datetime.strptime(row['time'].split(' ')[1], '%H:%M:%S' ))
    date = (row['time']).split(' ')[0]

dates = matplotlib.dates.date2num(timepoints)

data = np.genfromtxt(filename, delimiter=',', names=['x', 'y', 'z'])

fig, ax1 = plt.subplots()
ax1.plot(dates, data['y'], 'r-', linewidth=.5)
ax1.xaxis_date()
fig.autofmt_xdate()
ax1.set_ylabel('temp', color='r')
for tl in ax1.get_yticklabels():
    tl.set_color('r')
ax1.set_title(date)

ax2 = ax1.twinx()
ax2.plot(dates, data['z'], 'b-', linewidth=.5)
ax2.set_ylabel('hum', color='b')
for tl in ax2.get_yticklabels():
    tl.set_color('b')

fig.savefig(savename, bbox_inches='tight', dpi=200)

os.system("/home/pi/scripts/tg/sendpic.sh Alexander_Kutschera %s" %savename)
