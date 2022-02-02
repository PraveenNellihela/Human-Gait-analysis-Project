import os
from os import listdir
import numpy as np
import scipy.signal as signal
import pylab as plt
import pandas as pd


def low_pass():
    # ---------------------------------------- low_pass filter ---------------------------------------------#
    n = 3
    fc = 0.1
    b, a = signal.butter(n, fc, output='ba')
    filt_signal = signal.filtfilt(b, a, gyro_z)
    return filt_signal
    # ------------------------------------------------------------------------------------------------------#


def calculate_maximum():
    # ------------------------------------------ Maximum ---------------------------------------------------#
    for i in range(rows - 2):
        if new_signal[i] <= new_signal[i+1] >= new_signal[i+2]:
            if -15 <= new_signal[i+1] <= 60:
                first_max[i+1] = new_signal[i+1]
            elif new_signal[i+1] > 60:
                peak_max[i+1] = new_signal[i+1]
    # -----------------------------------------------------------------------------------------------------#


def calculate_minimum():
    # ------------------------------------------ Maximum --------------------------------------------------#
    for i in range(rows - 2):
        if new_signal[i] >= new_signal[i+1] <= new_signal[i+2]:
            if -50 <= new_signal[i+1] <= 50:
                first_mini[i+1] = new_signal[i+1]
            if new_signal[i+1] <= -50:
                peak_mini[i+1] = new_signal[i+1]
    # -----------------------------------------------------------------------------------------------------#


def end_of_swing_a():
    # ------------------------------------------ position a -----------------------------------------------#
    for i in range(rows - 2):
        if -20 <= new_signal[i+1] <= 20 and new_signal[i] > new_signal[i+1] > new_signal[i+2]:
            arr_a[i+1] = new_signal[i+1]
    # -----------------------------------------------------------------------------------------------------#


def mid_swing_e():
    # ------------------------------------------ position e -----------------------------------------------#
    for i in range(rows - 2):
        if -20 <= new_signal[i+1] <= 20 and new_signal[i] < new_signal[i+1] < new_signal[i+2] and new_signal[i+1] >= 0:
            arr_e[i+1] = new_signal[i+1]
    # -----------------------------------------------------------------------------------------------------#


def remove_invalids(count_steps):
    # remove values that appear before the first peak
    lim1 = df[df['position F'].notnull()].index[0]             # index of very first peak
    for x in range(len(df['position A'])):
        if df.loc[:, 'position F':'position D'].index[x] < lim1:
            df.loc[x, 'position A':'position E'] = np.nan
    # remove values that do not count as steps
    peak_array = list(df[df['position F'].notnull()].index)
    number_of_peaks = df[df['position F'].notnull()].index.size
    for y in range(number_of_peaks):
        try:
            if (df['time'].iloc[peak_array[y+1]]-df['time'].iloc[peak_array[y]]) < 1700:
                continue
            else:
                df.iloc[peak_array[y]+60: peak_array[y+1], 2:7] = np.nan
        except IndexError:      # exception occurs at final peak value.
            df.iloc[peak_array[y]+60:, 2:7] = np.nan

    # remove invalid position values of A, D and E
    pos_b_indices = list(df[df['position B'].notnull()].index)
    lim2 = df[df['position B'].notnull()].index.size
    for i in range(lim2):
        df.iloc[pos_b_indices[i]:pos_b_indices[i]+20, 3, ] = np.nan
        df.iloc[pos_b_indices[i] - 20:pos_b_indices[i], [5, 6]] = np.nan
    if count_steps:
        steps = number_of_peaks
        print(' number of steps = ', steps)


if __name__ == '__main__':
    path = 'C:/Users/PRAVEEN/Desktop/New folder'
    os.chdir(path)

    def find_csv_filenames(path, suffix=".csv"):
        filenames = listdir(path)
        return [filename for filename in filenames if filename.endswith(suffix)]

    filenames = find_csv_filenames(path)
    for name in filenames:
        # -------------- Import data ----------#
        data = np.genfromtxt(name,
                             delimiter=',',
                             skip_header=1, dtype=np.float)
        # -------------------------------------#

        # ------------- data setup ------------#
        gyro_z = data[:, 6]
        time = data[:, 0]
        rows = data.shape[0]  # no. of rows in array
        new_signal = list(np.zeros(rows))

        first_max = np.empty(rows)
        first_mini = np.empty(rows)
        peak_max = np.empty(rows)
        peak_mini = np.empty(rows)
        arr_e = np.empty(rows)
        arr_a = np.empty(rows)

        first_max[:] = np.nan
        first_mini[:] = np.nan
        peak_max[:] = np.nan
        peak_mini[:] = np.nan
        arr_e[:] = np.nan
        arr_a[:] = np.nan
        # -------------------------------------#

        # carry out operations
        new_signal = low_pass()
        calculate_maximum()
        calculate_minimum()
        end_of_swing_a()
        mid_swing_e()

        # add to data frame
        df = pd.DataFrame({'time': time, 'gyroZ': new_signal, 'position F': peak_max, 'position A': arr_a,
                           'position B': first_max, 'position D': peak_mini, 'position E': arr_e})

        # remove invalid values
        remove_invalids(count_steps=True)

        # plot graph
        ax1 = df.plot.line(x='time', y=[1, 2, 3, 4, 5, 6], style='-o', title=name)
        plt.show()
