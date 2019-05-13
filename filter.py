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

#------------- create table ----------#
#table = ff.create_table(data)
#py.offline.plot(table, filename='test table.html')
#-------------------------------------#

#------------- plot graph ------------#
trace1 = go.Scatter(x=list(time),y=list(gyro_z),mode='lines',name='original')
layout = go.Layout(showlegend=True)
trace_data = [trace1]
fig = go.Figure(data=trace_data, layout=layout)
plotly.offline.plot(fig, filename='data-plot.html')
#--------------------------------------#

#------------- LowPass filter ---------#
fc = 0.1
b = 0.08
N = int(np.ceil((4 / b)))
if not N % 2: N += 1
n = np.arange(N)

sinc_func = np.sinc(2 * fc * (n - (N - 1) / 2.))
window = 0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
sinc_func = sinc_func * window
sinc_func = sinc_func / np.sum(sinc_func)

s = list(gyro_z)
new_signal = np.convolve(s, sinc_func)

trace1 = go.Scatter(x=list(range(len(new_signal))),y=new_signal,mode='lines',name='Low-Pass Filter',marker=dict(color='#C54C82'))

layout = go.Layout(
    title='Low-Pass Filter',
    showlegend=True
)

trace_data = [trace1]
fig = go.Figure(data=trace_data, layout=layout)
plotly.offline.plot(fig, filename='fft-low-pass-filter.html')
#--------------------------------------#


#------------- function ---------------#

#--------------------------------------#