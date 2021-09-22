 # -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 23:07:10 2020

@author: lesli
"""

import diff
import fitdata
import matplotlib.pyplot as plt
import matplotlib
matplotlib.axes.Axes.plot
matplotlib.pyplot.plot
matplotlib.axes.Axes.legend
matplotlib.pyplot.legend
import numpy as np


time, vel, alt = np.loadtxt("rocket.dat") 
acc = diff.finite_diff(time, vel) #this is the estimate of the acceleration based on finite difference approximations using the data
#--------------------------------------------------------------

"""
    In this section the code provides an  estimate of the acceleration based on various polynomial fits. 

"""
int_count = 9 #8 intervals containing 66 elements each are created here.
increment = 66
int_bound = np.zeros(int_count)

sum1 = 0
for i in range(int_count):
    int_bound[i] = sum1
    sum1 += increment #intervals boundaries are set here
    

xdat = np.zeros(increment)
ydat = np.zeros(increment)

acc2 = [] #empty list that will store acceleration values
degrees = np.array([5,6,3,5,6,3,6,5]) 

for i in range(0,int_count-1):
    min_num = int_bound[i]
    max_num = int_bound[i+1]

    x = int(min_num)
    y = int(max_num)
    
    xdat = time[x:y]
    ydat = vel[x:y]
    
    deg = degrees[i]
    coeff = fitdata.calc_fit(xdat, ydat, degree = deg)
    yfit = diff.polynomial_derivative(coeff,xdat)
    for k in range(yfit.size):
        acc2.append(yfit[k])
        
arr_acc2 = np.array(acc2) #list is converted into an array  
#arr_acc2 is an array that contains acceleration values that were estimated using polynomial fits

#------------------------------------------------------------

"""

    This section of code contains 2 different functions that measure the difference 
between two equal length vectors of n data points

"""
def MAD(arr1,arr2):
    n = arr1.size
    
    sum = 0.0
    for i in range(n):
        sum += abs(arr1[i]-arr2[i])
        
    return (1/n)*sum
    
    
def RMSD(arr1,arr2):
    n = arr1.size
    
    sum = 0.0
    for i in range(n):
        sum += (abs(arr1[i]-arr2[i]))**2
        
    return ((1/n)*sum)**(1/2)

mad = MAD(acc,arr_acc2)
#print(mad)        
rmsd = RMSD(acc,arr_acc2)
#print(rmsd)

#---------------------------------------
"""
     This section is dedicated to plotting the velocity and the 2 types of acceleration that were previously obtained

"""
data1 = vel
data2 = acc
data3 = arr_acc2


fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity(m/s)', color=color)
ax1.plot(time, data1, color=color, label='Velocity')
ax1.tick_params(axis='y', labelcolor=color)
legend = ax1.legend(loc=4, shadow=True, fontsize='small')

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'b'
ax2.set_ylabel('acceleration(m/s^2)', color=color)  # we already handled the x-label with ax1
ax2.plot(time, data2, 'b', label = 'Acceleration (finite difference approximation)')
ax2.plot(time, data3, 'b--', label = 'Acceleration(polynomial fit)')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
ax1.set_title('Aleman, Leslie (alemal2)' + '\n' + 'MAD:' + str('{:8.5f}'.format(mad)) + '  ' + 'RMSD:' + str('{:8.5f}'.format(rmsd)) , fontsize=16)
legend = ax2.legend(loc='best', shadow=True, fontsize='small')
plt.show()
fig.savefig('hw6_plot.png', dpi=300, bbox_inches='tight', edgecolor='none')

