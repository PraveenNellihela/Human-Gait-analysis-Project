import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from scipy import signal
import plotly
import plotly.graph_objs as go

#-------------- Import data ----------#
data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#-------------------------------------#

#------------- data setup ------------#
gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]    #no. of rows in array
#table = ff.create_table(data)
#py.offline.plot(table, filename='test table.html')
#-------------------------------------#

#------------- plot grapha -----------#
trace1 = go.Scatter(
    x=list(time),
    y=list(gyro_z),
    mode='lines',
    name='original'
)
layout = go.Layout(showlegend=True)

trace_data = [trace1]
fig = go.Figure(data=trace_data, layout=layout)
plotly.offline.plot(fig, filename='data-plot.html')
