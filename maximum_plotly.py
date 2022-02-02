import numpy as np
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

# -------------- Import data ----------#
data = np.genfromtxt("D:/Humain_gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',',
                     skip_header=1, dtype=np.float)
# data [row,column], zero indexed  # extract entire column [:, x] #extract entire row [x,:]
# -------------------------------------#

# ------------- data setup ------------#
gyro_z = data[:, 6]
time = data[:, 0]
rows = data.shape[0]  # no. of rows in array
# -------------------------------------#

# ------- initialize numpy arrays -----#
dif = np.zeros((rows, 1))
max_number = np.zeros((rows, 1))
maximum = np.empty((rows, 1))
# -------------------------------------#

for i in range(rows - 2):
    # --------- Differentiation -------#
    # v_dif = gyro_z[i+1]- gyro_z[i]
    # t_dif = time[i+1] - time[i]
    # dif[i] = v_dif/t_dif
    # ---------------------------------#

    # --------- Maximum ---------------#
    if gyro_z[i] < gyro_z[i + 1] and gyro_z[i + 1] > gyro_z[i + 2]:
        max_number[i] = 1  # iterable for total maximums
        maximum[i + 1] = gyro_z[i + 1]
    # ---------------------------------#

print('total number of maximums =', sum(max_number))

trace = go.Scatter(
    x=time,
    y=maximum,
    mode='lines'
)

data = [trace]
py.plot(data, filename='file_name.html')
