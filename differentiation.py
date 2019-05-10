import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#print(data[:,6])                            # data [row,column], zero indexed  # extract entire column [:, x] #extract entire row [x,:]
#print(data.shape)

gyro_z = data[:,6]
time = data [:, 0]
print(data.shape)
rows = data.shape[0]

print('Gyro', gyro_z)
print('time', time [:5])
dif = np.zeros((rows, 1))
for i in range (rows-1):
    v_dif = gyro_z[i+1]- gyro_z[i]
    t_dif = time[i+1] - time[i]
    dif[i] = v_dif/t_dif

print(dif)

plt.plot(time, dif)
plt.show()