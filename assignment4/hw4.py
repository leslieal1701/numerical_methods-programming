# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 17:18:46 2020

@author: lesli
"""
import numpy as np
import fitdata
import random
import matplotlib.pyplot as plt

int_count = 9
increment = 66
int_bound = np.zeros(int_count)

sum1 = 0
for i in range(int_count):
    int_bound[i] = sum1
    sum1 += increment
    


time, vel, alt = np.loadtxt("rocket.dat") 

xdat = np.zeros(increment)
ydat = np.zeros(increment)
#----------------------------------------------

plt.figure(1, figsize=(8,6))
plt.plot(time,vel, 'k', label = 'raw velocity' )


for i in range(0,int_count-1):
    min_num = int_bound[i]
    max_num = int_bound[i+1]

    x = int(min_num)
    y = int(max_num)
    
    xdat = time[x:y]
    ydat = vel[x:y]
    
    rand_deg = random.randint(1,3)

    coeff = fitdata.calc_fit(xdat, ydat, degree = rand_deg)
    yfit = fitdata.eval_fit(coeff,xdat) 
    plt.plot(xdat, yfit, 'ro', label='[ ' + str(x) + ', ' + str(y) + '): ' + 'P' + str(rand_deg),  mfc='w' ) #poly fit data
           
    
xlow = 0
xhigh = 600
ylow = 0
yhigh = 8000
plt.axis([xlow, xhigh, ylow, yhigh])
plt.title('Aleman, Leslie (alemal2)')
# label the x- and y-axes
plt.xlabel('Time (s) ', fontsize=14)
plt.ylabel('Velocity (m/s)', fontsize=14)
plt.legend(fontsize=14, loc=4) # add a legend
plt.gca().grid()
plt.savefig('hw4_plot.png', dpi=300, edgecolor='none')