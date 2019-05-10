import numpy as np
import matplotlib.pyplot as plt

#-------------- Import data ----------#
data = np.genfromtxt("D:/Work/SLIIT/Humain gait/data/New Analysis/MAL/200 Steps/IMU Data/new_F1T1.csv", delimiter=',', skip_header=1, dtype=np.float)
# data [row,column], zero indexed  # extract entire column [:, x] #extract entire row [x,:]
#-------------------------------------#

#------------- data setup ------------#
gyro_z = data[:,6]
time = data [:, 0]
rows = data.shape[0]    #no. of rows in array
#-------------------------------------#

#------- initialize numpy arrays -----#
dif = np.zeros((rows, 1))
max_number = np.zeros((rows, 1))
maximum = np.zeros((rows,1))
#-------------------------------------#

for i in range (rows-2):
    #--------- Differentiation -------#
    #v_dif = gyro_z[i+1]- gyro_z[i]
    #t_dif = time[i+1] - time[i]
    #dif[i] = v_dif/t_dif
    #---------------------------------#

    #--------- Maximum ---------------#
    if gyro_z[i] < gyro_z[i+1] and gyro_z[i+1] > gyro_z[i+2] :
        max_number[i]= 1                 #iterable for total maximums
        maximum[i+1] = gyro_z[i+1]
    #---------------------------------#

print('total number of maximums =',sum(max_number))

#----------- Plot setup --------------#
plt.plot(time,gyro_z, label = "original")
plt.plot(time,maximum, label = "maximum")
plt.xlabel('x - axis')
plt.ylabel('y - axis')
plt.title('original vs. maximums ')
plt.legend()
#----------- Display plot ------------#
plt.show()
#-------------------------------------#
