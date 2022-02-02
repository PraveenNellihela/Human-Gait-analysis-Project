import numpy as np
import scipy.signal as signal
from bokeh.plotting import figure, output_file, show

# -------------- Import data ----------#
data = np.genfromtxt("D:/Humain_gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',',
                     skip_header=1, dtype=np.float)
# -------------------------------------#

# ------------- data setup ------------#
gyro_z = data[:, 6]
time = data[:, 0]
rows = data.shape[0]  # no. of rows in array

# maximum = list(np.zeros(rows)) # initialize maximum array
new_signal = list(np.zeros(rows))
# -------------------------------------#


def plot_graph(file_name, title, x_label, y_label, legend, x_var, y_var):
    # ------------- plot graph ------------#
    output_file(file_name)  # output to static HTML file
    p = figure(title=title, x_axis_label=x_label, y_axis_label=y_label,
               sizing_mode="stretch_both")  # create a new plot with a title and axis labels
    p.line(x_var, y_var, legend=legend, line_width=2)  # add a line renderer with legend and line thickness
    show(p)                 # show the results
    # --------------------------------------#


def plot_multigraph(x1, y1, l1, c1, x2, y2, l2, c2, x_label='x axis', y_label='y axis', cond='False'):
    # --------------------------------- plot multiple graphs in one ---------------------------------------#
    output_file("multi_graph.html")  # output to static HTML file
    # create a new plot
    p = figure(
        tools="pan,box_zoom,reset,save",
        x_axis_label=x_label, y_axis_label=y_label,
        sizing_mode="stretch_both"
    )
    # add some renderers
    original = cond                 # plot original data conditionally
    if original == True:
        p.line(time, gyro_z, legend="original", line_color='green')
        p.circle(time, gyro_z, legend="original", fill_color='white', line_color='green', size=4)

    p.line(x1, y1, legend=l1, line_color=c1)
    p.circle(x1, y1, legend=l1, fill_color="white", size=8)

    p.line(x2, y2, legend=l2, line_color=c2)
    p.circle(x2, y2, legend=l2, fill_color=c2, line_color=c2, size=6)
    # show the results
    show(p)
    # -----------------------------------------------------------------------------------------------------#


def plot_original():
    # ------------------------------------------ plot graph -----------------------------------------------#
    plot_graph('original.html', 'original data plot', 'time', 'gyro_z', 'Original data', time, gyro_z)
    # -----------------------------------------------------------------------------------------------------#


def LowPass():
    # ---------------------------------------- LowPass filter ---------------------------------------------#
    N = 3
    fc = 0.1
    B, A = signal.butter(N, fc, output='ba')
    filt_signal = signal.filtfilt(B, A, gyro_z)
    return filt_signal
    # ------------------------------------------------------------------------------------------------------#


def calculate_maximum():
    # ------------------------------------------ Maximum ---------------------------------------------------#
    maxi = np.zeros(rows)
    for i in range(rows - 2):
        if new_signal[i] <= new_signal[i + 1] >= new_signal[i + 2] and -10 <= new_signal[i + 1] <= 30:
            maxi[i + 1] = new_signal[i + 1]
    return maxi
    # -----------------------------------------------------------------------------------------------------#


def calculate_mimimum():
    # ------------------------------------------ Maximum --------------------------------------------------#
    mini = np.zeros(rows)
    for i in range(rows - 2):
        if new_signal[i] >= new_signal[i + 1] <= new_signal[i + 2] and -50 <= new_signal[i + 1] <= 50:
            mini[i + 1] = new_signal[i + 1]
    return mini
    # -----------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    # ------------------------------------------ MAIN -----------------------------------------------------#

    new_signal = LowPass()
    maximum = calculate_maximum()
    minimum = calculate_mimimum()
    plot_multigraph(time, new_signal, 'low pass data', 'blue', time, maximum, 'maximum', 'red', 'time', 'gyro data',
                    cond=True)
    plot_multigraph(time, new_signal, 'low pass data', 'blue', time, minimum, 'minimum', 'orange', 'time', 'gyro data',
                    cond=True)
