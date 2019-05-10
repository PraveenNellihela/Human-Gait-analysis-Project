import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
#print(data[:,6])                            # data [row,column], zero indexed  # extract entire column [:, x] #extract entire row [x,:]
#print(data.shape)

gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]
print('array size =',data.shape)

dif = np.zeros((rows, 1))
max_number = np.zeros((rows, 1))
maximum = np.zeros((rows,1))
testT = np.zeros((rows,1))
for i in range (0,rows-1,3):
    #v_dif = gyro_z[i+1]- gyro_z[i]
    #t_dif = time[i+1] - time[i]
    #dif[i] = v_dif/t_dif
    #--------- Maximum ---------------#
    if gyro_z[i] < gyro_z[i+1] and gyro_z[i+1] > gyro_z[i+2] :
        max_number[i]= 1                 #iterable for total maximums
        maximum[i+1] = gyro_z[i+1]
        testT[i+1] = time[i+1]

print(i)
print(gyro_z[i])
print(gyro_z[i+2])
#print(dif)
print('total number of maximums =',sum(max_number))
print(maximum[i+1])
#plt.plot(time, dif)
#plt.show()

plt.plot(time,gyro_z, label = "original")
plt.plot(time,maximum, label = "maximum")

plt.xlabel('x - axis')
# Set the y axis label of the current axis.
plt.ylabel('y - axis')
# Set a title of the current axes.
plt.title('original vs. maximums ')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.show()
