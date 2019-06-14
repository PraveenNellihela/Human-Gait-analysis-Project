import numpy as np
import scipy.signal as signal
from bokeh.plotting import figure, output_file, show
import pandas as pd
#-------------- Import data ----------#
data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#-------------------------------------#

#------------- data setup ------------#
gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]        #no. of rows in array

#maximum = list(np.zeros(rows)) # initialize maximum array
new_signal = list(np.zeros(rows))
#-------------------------------------#
first_max = np.empty(rows)
peak_max = np.empty(rows)
first_mini = np.empty(rows)
peak_mini = np.empty(rows)
arr_e = np.empty(rows)
arr_a = np.empty(rows)
begin = 0
end = 200

def plot_graph(file_name, title, x_label, y_label, legend,x_var, y_var):
    #------------- plot graph ------------#
    output_file(file_name)                                              # output to static HTML file
    p = figure(title=title, x_axis_label=x_label, y_axis_label=y_label, sizing_mode= "stretch_both" ) # create a new plot with a title and axis labels
    p.line(x_var, y_var, legend=legend, line_width=2)                   # add a line renderer with legend and line thickness
    show(p)                                                             # show the results
    #--------------------------------------#

def plot_multigraph(filename, x1, y1, l1, c1, x2, y2, l2, c2,  x_label = 'x axis', y_label='y axis',cond ='False'):
    #--------------------------------- plot multiple graphs in one ---------------------------------------#
    output_file(filename)                                         # output to static HTML file
                                                                            # create a new plot
    p = figure(
        tools="pan,box_zoom,reset,save",
        x_axis_label=x_label, y_axis_label=y_label,
        sizing_mode = "stretch_both"
    )
                                                                            # add some renderers
    original = cond                                                         # plot original data conditionally
    if original == True:
        p.line(time, gyro_z, legend="original", line_color='green')
        p.circle(time, gyro_z, legend="original", fill_color='white', line_color='green', size=4)

    p.line(x1, y1, legend=l1, line_color=c1)
    p.circle(x1, y1, legend=l1, fill_color="white", size=8)

    p.line(x2, y2, legend=l2, line_color=c2)
    p.circle(x2, y2, legend=l2, fill_color=c2, line_color=c2, size=6)
                                                                        # show the results
    show(p)
    #-----------------------------------------------------------------------------------------------------#

def all_positions(filename, x1, y1, c1, y2, c2,  y3,c3, y4,c4,y5,c5, l1,l2,l3,l4,l5, x_label = 'x axis', y_label='y axis',cond_original ='False', cond_filtered='False'):
    #--------------------------------- plot multiple graphs in one ---------------------------------------#
    output_file(filename)                                         # output to static HTML file
                                                                            # create a new plot
    p = figure(
        tools="pan,box_zoom,reset,save",
        x_axis_label=x_label, y_axis_label=y_label,
        sizing_mode = "stretch_both"
    )
                                                                            # add some renderers
    original = cond_original                                                         # plot original data conditionally
    if original == True:
        p.line(time, gyro_z, legend="original", line_color='green')
        p.circle(time, gyro_z, legend="original", fill_color='white', line_color='green', size=4)

    filter = cond_filtered  # plot original data conditionally
    if filter == True:
        p.line(time, new_signal, legend="original", line_color='green')
        p.circle(time, new_signal, legend="original", fill_color='white', line_color='green', size=5)

    p.line(x1, y1, legend=l1, line_color=c1)
    p.circle(x1, y1, legend=l1, fill_color=c1, size=8)

    p.line(x1, y2, legend=l2, line_color=c2)
    p.circle(x1, y2, legend=l2, fill_color=c2, line_color=c2, size=8)

    p.line(x1, y3, legend=l3, line_color=c3)
    p.circle(x1, y3, legend=l3, fill_color=c3, size=8)

    p.line(x1, y4, legend=l4, line_color=c4)
    p.circle(x1, y4, legend=l4,  line_color=c4, size=8)

    p.line(x1, y5, legend=l5, line_color=c5)
    p.circle(x1, y5, legend=l5,  fill_color=c5, line_color=c5, size=8)
                                                                        # show the results
    show(p)




def plot_original():
    #------------------------------------------ plot graph -----------------------------------------------#
    plot_graph('original.html', 'original data plot', 'time','gyro_z', 'Original data', time, gyro_z)
    #-----------------------------------------------------------------------------------------------------#

def LowPass():
    #---------------------------------------- LowPass filter ---------------------------------------------#

    N = 3
    fc = 0.1
    B, A = signal.butter(N, fc, output='ba')
    filt_signal = signal.filtfilt(B, A, gyro_z)

    return filt_signal

    #------------------------------------------------------------------------------------------------------#


def calculate_maximum():
    #------------------------------------------ Maximum ---------------------------------------------------#
    for i in range(rows - 2):
        if new_signal[i] <= new_signal[i+1] >= new_signal[i+2]:
            if -10<=new_signal[i+1]<=30:
                first_max[i+1] = new_signal[i+1]
            elif new_signal[i+1]>50:
                peak_max[i+1] = new_signal[i+1]
    #-----------------------------------------------------------------------------------------------------#

def calculate_mimimum():
    #------------------------------------------ Maximum --------------------------------------------------#
    for i in range(rows - 2):
        if new_signal[i] >= new_signal[i+1] <= new_signal[i+2]:
            if -50<=new_signal[i+1]<=50:
                first_mini[i+1] = new_signal[i+1]
            if new_signal[i+1]<=-50:
                peak_mini[i+1] = new_signal[i+1]
    #-----------------------------------------------------------------------------------------------------#

def end_of_swing_A():
    #------------------------------------------ position a -----------------------------------------------#

    for i in range(rows - 2):
        if -20<= new_signal[i+1] <=20 and new_signal[i]>new_signal[i+1]>new_signal[i+2] and new_signal[i+1]>=0:
            arr_a[i+1] = new_signal[i+1]

    #-----------------------------------------------------------------------------------------------------#

def mid_swing_E():
    #------------------------------------------ position a -----------------------------------------------#

    for i in range(rows - 2):
        if -20<= new_signal[i+1] <=20 and new_signal[i]<new_signal[i+1]<new_signal[i+2] and new_signal[i+1]>=0 :
            arr_e[i+1] = new_signal[i+1]
    #-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    #------------------------------------------ MAIN -----------------------------------------------------#
    new_signal = LowPass()

    calculate_maximum()
    calculate_mimimum()
    end_of_swing_A()
    mid_swing_E()

    #all_positions('all_positions.html', time, peak_max, 'red', first_max, 'black', peak_mini, 'orange', arr_a, 'blue', arr_e, 'pink', 'position f', 'position b','position d','position a','position e',cond_filtered=True)
    '''
    plot_multigraph('maximum.html',time, new_signal, 'low pass data', 'blue', time, peak_max, 'maximum', 'red', 'time','gyro data')
    plot_multigraph('minimum.html', time, new_signal, 'low pass data', 'blue', time, first_max, 'position b', 'orange','time', 'gyro data')
    plot_multigraph('minimum.html',time, new_signal, 'low pass data', 'blue', time, peak_mini, 'position d', 'green', 'time','gyro data')
    plot_multigraph('eos.html',time, new_signal, 'low pass data', 'blue', time, position_a, 'end of swing (position a)', 'purple', 'time', 'gyro data')
    '''

    dataframe = pd.DataFrame({'time': time, 'filtered gyro Z': new_signal, 'maximum peak(F)': peak_max, 'zero crossing (A)': arr_a,'maximum zero(B)': first_max,'peak minimum (D)':peak_mini,'mid swing(E)':arr_e})
    print(dataframe)

# f to a  time 200
