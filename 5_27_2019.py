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
rows = data.shape[0]        #no. of rows in array
maximum = np.zeros((rows, 1))  # initialize maximum array
pos_b = np.zeros((rows, 1))  # initialize maximum array
#-------------------------------------#
def data_table():
    #------------- create table ----------#
    table = ff.create_table(data)
    py.offline.plot(table, filename='test table.html')
    #-------------------------------------#
def plot_graph(x_var, y_var, plot_name, file_name, color='#1f77b4'):
    #------------- plot graph ------------#
    trace1 = go.Scatter(x=list(x_var),y=list(y_var),mode='lines+markers',name=plot_name, marker=dict(color=color))
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

    for i in range(rows - 2):
        if new_signal[i] <= new_signal[i+1] <= new_signal[i+2]:
            if 20 <= new_signal[i+1] <= -20:
                new_signal[i+1] = pos_b[i+1]

    plot_graph(range(len(pos_b)),pos_b,'Low-Pass Filter', 'test mnaximum.html','#C54C82')
    #--------------------------------------#
def calculate_maximum():
    #--------- Maximum ---------------#
    for i in range(rows - 2):
        if gyro_z[i] < gyro_z[i+1] and gyro_z[i+1] > gyro_z[i+2] :
            maximum[i+1] = gyro_z[i+1]
    plot.plot(time, maximum, label="maximum")
    plt.show()
    #---------------------------------#
if __name__ == '__main__':
    #--------- MAIN -------------------#
    #plot_graph(time, gyro_z, 'Original', 'original data plot.html') #plot original
    plot_LowPass()                                                  #plot lowpass
    #print(maximum)
    #calculate_maximum()
    #print(maximum)
    #plot_graph(range(len(maximum)),maximum, 'maximum plot', 'maximum.html')

#------------- function ---------------#

#--------------------------------------#