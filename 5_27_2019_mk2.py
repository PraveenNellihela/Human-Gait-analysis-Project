import numpy as np

import plotly.plotly as py
import plotly.graph_objs as go

from scipy.signal import argrelextrema

#-------------- Import data ----------#
data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#-------------------------------------#

#------------- data setup ------------#
gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]        #no. of rows in array

maximum = np.empty((rows, 1))  # initialize maximum array
pos_b = np.empty((rows, 1))  # initialize maximum array
new_signal = np.empty((rows,1))
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
    py.plot(fig, filename=file_name)
    #--------------------------------------#
def plot_multigraph(x, y1, y2, plot_name, file_name,color1='#1f77b4',color2='#000000'):
    #------------- plot graph ------------#
    trace1 = go.Scatter(x=list(x),y=list(y1),mode='lines', marker=dict(color=color1))
    trace2 = go.Scatter(x=list(x), y=list(y2), mode='lines+markers', marker=dict(color=color2))

    layout = go.Layout(title=plot_name, showlegend=True)
    trace_data = [trace1, trace2]
    fig = go.Figure(data=trace_data, layout=layout)
    py.plot(fig, filename=file_name)
    #py.plot(trace_data, filename=file_name)
    #--------------------------------------#
def plot_original():
    #------------- plot graph ------------#
    plot_graph(time, gyro_z, 'Original data plot', 'Original data plot.html', '#000000')
    #--------------------------------------#
def plot_LowPass(plot=False):
    plot=plot
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

    if plot:
        plot_graph(time, new_signal, 'lowpass filter', 'lowpass plot.html', '#FF6347')

    #pos_b = new_signal[argrelextrema(new_signal, np.greater)[0]]
    #plot_graph(time, pos_b, 'position test', 'position test.html', '#C54C82')
    #--------------------------------------#
def calculate_maximum(plot=False):
    #--------- Maximum ---------------#
    plot=plot
    for i in range(rows - 2):
        if gyro_z[i] <= gyro_z[i+1] >= gyro_z[i+2] and -10<=gyro_z[i+1]<=30 :
            maximum[i+1] = gyro_z[i+1]

    if plot:
        plot_multigraph(time, new_signal, maximum, 'combined plot', 'combined plot.html')
        #plot_graph(time, maximum, 'maximum', 'maximum plot.html')

    #pos_b = new_signal[argrelextrema(new_signal, np.greater)[0]]
    #plot_graph(time, pos_b, 'position test', 'position test.html', '#C54C82')
    #---------------------------------#
if __name__ == '__main__':
    #--------- MAIN -------------------#
    #plot_graph(time, gyro_z, 'Original', 'original data plot.html') #plot original
    #plot_original()
    plot_LowPass()                                                  #plot lowpass
    calculate_maximum(True)


    #print(maximum)
    #calculate_maximum()
    #print(maximum)
    #plot_graph(range(len(maximum)),maximum, 'maximum plot', 'maximum.html')

#------------- function ---------------#

#--------------------------------------#
