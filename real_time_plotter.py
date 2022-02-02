import numpy as np
import scipy.signal as signal
from bokeh.io import curdoc
from bokeh.plotting import figure, output_file, show
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema, find_peaks

output_file('temp.html')


def LowPass(filterData):
    # ---------------------------------------- LowPass filter ---------------------------------------------#
    N = 3
    fc = 0.1
    B, A = signal.butter(N, fc, output='ba')
    filt_signal = signal.filtfilt(B, A, filterData)
    return filt_signal
    # ------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':
    sel = 200  # iterator to get data section by section
    start = 0
    plt.ion()
    while sel < 1600:
        with open("D:/Humain_gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv") as f_in:
            x = np.genfromtxt(itertools.islice(f_in, start, sel), delimiter=',', dtype=np.float)

        # create data frame
        time = x[:, 0]
        gyro_Z = x[:, 6]
        GyroFilt = LowPass(gyro_Z)
        df = pd.DataFrame({'time': time, 'gyroZ': GyroFilt})

        # Find local peaks
        pos_f = 50  # minimum value to detect peak
        n = 5       # number of points to be checked before and after

        df['min'] = df.iloc[argrelextrema(df.gyroZ.values, np.less_equal, order=n)[0]]['gyroZ']
        df['max'] = df.iloc[argrelextrema(df.gyroZ.values, np.greater_equal, order=n)[0]]['gyroZ']
        df['peak'] = df.iloc[find_peaks(df.gyroZ.values, height=pos_f)[0], :]['gyroZ']
        print(df)

        # Plot results
        plt.scatter(df['time'], df['min'], c='g')
        plt.scatter(df['time'], df['max'], c='y')
        plt.scatter(df['time'], df['peak'], c='r')
        plt.plot(df['time'], df['gyroZ'])
        plt.draw()
        plt.pause(0.5)

        start = sel + 1
        sel = sel + 201

    plt.show(block=True)
