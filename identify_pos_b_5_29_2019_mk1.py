import numpy as np

from bokeh.plotting import figure, output_file, show

#-------------- Import data ----------#
data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#-------------------------------------#

#------------- data setup ------------#
gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]        #no. of rows in array

maximum = np.zeros((rows, 1))  # initialize maximum array
pos_b = np.empty((rows, 1))  # initialize maximum array
new_signal = np.empty((rows,1))
#-------------------------------------#

def plot_graph(file_name, title, x_label, y_label, legend,x_var, y_var):
    #------------- plot graph ------------#
    output_file(file_name)                                              # output to static HTML file
    p = figure(title=title, x_axis_label=x_label, y_axis_label=y_label) # create a new plot with a title and axis labels
    p.line(x_var, y_var, legend=legend, line_width=2)                   # add a line renderer with legend and line thickness
    show(p)                                                             # show the results
    #--------------------------------------#

def plot_multigraph(x1, y1, l1, c1, x2, y2, l2, c2,  x_label = 'x axis', y_label='y axis'):
    #--------------------------------- plot multiple graphs in one ---------------------------------------#
    output_file("log_lines.html")                                       # output to static HTML file
                                                                        # create a new plot
    p = figure(
        tools="pan,box_zoom,reset,save",
        x_axis_label=x_label, y_axis_label=y_label
    )
                                                                     # add some renderers
    p.line(x1, y1, legend=l1)
    p.circle(x1, y1, legend=l1, fill_color=c1, size=8)

    p.line(x2, y2, legend=l2, line_color=c2)
    p.circle(x2, y2, legend=l2, fill_color=c2, line_color=c2, size=6)
                                                                        # show the results
    show(p)
    #-----------------------------------------------------------------------------------------------------#

def plot_original():
    #------------------------------------------ plot graph -----------------------------------------------#
    plot_graph('original.html', 'original data plot', 'time','gyro_z', 'Original data', time, gyro_z)
    #-----------------------------------------------------------------------------------------------------#

def plot_LowPass(plot=False):
    plot=plot
    #---------------------------------------- LowPass filter ---------------------------------------------#
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
    #------------------------------------------------------------------------------------------------------#

def calculate_maximum(plot=False):
    #------------------------------------------ Maximum ---------------------------------------------------#
    plot=plot
    for i in range(rows - 2):
        if gyro_z[i] <= gyro_z[i+1] >= gyro_z[i+2] and -10<=gyro_z[i+1]<=30:
            maximum[i+1] = gyro_z[i+1]

    if plot:
        plot_graph("maximum.html","maximum plot",'time','maximum points', 'maximum', time, maximum[:,0] )
        print(maximum)
        #plot_multigraph(time, new_signal, maximum, 'combined plot', 'combined plot.html')
        #plot_graph(time, maximum, 'maximum', 'maximum plot.html')

    #pos_b = new_signal[argrelextrema(new_signal, np.greater)[0]]
    #plot_graph(time, pos_b, 'position test', 'position test.html', '#C54C82')
    #-----------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    #------------------------------------------ MAIN -----------------------------------------------------#

    plot_original()                                                     #plot original
    #plot_LowPass()                                                     #plot lowpass
    calculate_maximum(True)

    plot_multigraph(time,gyro_z,'original data','blue', time, maximum[:,0],'maximum','red','time', 'gyro data')


