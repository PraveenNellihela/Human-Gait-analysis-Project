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
#-------------------------------------#
def data_table():
    #------------- create table ----------#
    table = ff.create_table(data)
    py.offline.plot(table, filename='test table.html')
    #-------------------------------------#
def plot_graph(x_var, y_var, plot_name, file_name, color='#1f77b4'):
    #------------- plot graph ------------#
    trace1 = go.Scatter(x=list(x_var),y=list(y_var),mode='lines',name=plot_name, marker=dict(color=color))
    layout = go.Layout(title=plot_name, showlegend=True)
    trace_data = [trace1]
    fig = go.Figure(data=trace_data, layout=layout)
    plotly.offline.plot(fig, filename=file_name)
    #--------------------------------------#
def plot_LowPass():
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

    plot_graph(range(len(new_signal)),new_signal,'Low-Pass Filter', 'low pass filter.html','#C54C82')
    #--------------------------------------#
def maximum():
    #--------- Maximum ---------------#
    if gyro_z[i] < gyro_z[i+1] and gyro_z[i+1] > gyro_z[i+2] :
        max_number[i]= 1                 #iterable for total maximums
        maximum[i+1] = gyro_z[i+1]
    #---------------------------------#

if __name__ == '__main__':
    #--------- MAIN -------------------#
    plot_graph(time, gyro_z, 'Original', 'original data plot.html') #plot original
    plot_LowPass()                                                  #plot lowpass




#------------- function ---------------#

#--------------------------------------#