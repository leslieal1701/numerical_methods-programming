""" A module for finding the distance travelled by the SpaceX Falcon Heavy rocket"""
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 23:16:25 2020

@author: lesli
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.axes.Axes.plot
matplotlib.pyplot.plot
matplotlib.axes.Axes.legend
matplotlib.pyplot.legend
import matplotlib.ticker as tick
from quadrature import gauss_quad
import fitdata

"""
    This section of code is dedicated to plotting the distance travelled by
    calculating the change in velocity over the change in time
"""
time, vel, alt = np.loadtxt("rocket.dat")
N = time.size
delta_t = np.zeros(time.size-1)
n = delta_t.size
distance = np.zeros(N)

#an array containing successieve changes in time is created here
for i in range(n):
    delta_t[i] = time[i+1] - time[i]
#print(delta_t)

#change in velocity over change in time is calculated here and stored in a distance array
sum = 0.0
for k in range(1,N):
    sum += (vel[k] + vel[k-1]) * (delta_t[k-1]/2)
    distance[k] = sum


#plotting begins        
data1 = vel
data2 = distance
min_x = 0
max_x = 528
min_y = 0
max_y = 7500
min_y2 = 0
max_y2 = 1.72e+06

fig, ax1 = plt.subplots()

color = 'tab:red'
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Velocity(m/s)', color=color)
line1, = ax1.plot(time, data1, color=color)
ax1.tick_params(axis='y', labelcolor=color)
plt.grid(True)


plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y) 
ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
ax2.set_ylim(min_y2, max_y2)
y_fmt = tick.FormatStrFormatter('%.2E')
ax2.yaxis.set_major_formatter(y_fmt)

color = 'b'
ax2.set_ylabel('Distance (m)', color=color)  # we already handled the x-label with ax1
line2, = ax2.plot(time, data2, 'b')
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
fig.suptitle('The plotted distance data points were derived by ' + '\n'
             + 'employing the integration technique of approximating' + '\n'
             + ' the trapezoidal area in each time interval' + '\n'
             + ' ', fontname='Times New Roman', fontsize=12) 
plt.legend((line1,line2),("Falcon Heavy launch velocity data","Total Distance Travelled"),fontsize = 10)
fig.tight_layout()
fig.subplots_adjust(top=0.82)
plt.show()
fig.savefig('hw7_plot.png', dpi=300,bbox_inches='tight', edgecolor='none')

"""
The plotted distance data points were derived by integrating the velocity data as a function of time for the given time intervals.
The integration technique employed consisted of approximating the area in each interval by a trapezoid. Each individual distance element
 is the integral of the velocity up to a given time, that is the sum of the trapazoids up to that time.

"""
#-----------------------------------------

def polynomial_integral(coef, a, b):
    '''
        Returns the total distance travelled. Computes distance by “manually” integrating the velocity data 
        Parameters:
        - coef:a 1D NumPy array of polynomial coefficients in the order c0, c1, c2,...
        -a and b: scalar floats between which to calculate the integral of the polynomial
    '''
    n = coef.size
    integral_a = 0.0
    integral_b = 0.0
    for i in range(n-1, -1, -1):
        integral_a += coef[i] * (a**(i+1) / (i+1))
        integral_b += coef[i] * (b**(i+1) / (i+1))     
    return integral_b - integral_a 

#---------------------------------------------
''' 
    This section of code is dedicated to calculating the total distance travelled by using polynomial fits
'''
int_count = 9 #8 intervals containing 66 elements each are created here.
increment = 66
int_bound = np.zeros(int_count)

sum1 = 0
for i in range(int_count):
    int_bound[i] = sum1
    sum1 += increment #intervals boundaries are set here
    

xdat = np.zeros(increment)
ydat = np.zeros(increment)

degrees = np.array([5,6,3,5,6,3,6,5]) 
sum1 = 0.0

distance = 0.0
for i in range(0,int_count-1): #8 iterations
    min_num = int_bound[i]
    max_num = int_bound[i+1]


    x = int(min_num)
    y = int(max_num)
    
    xdat = time[x:y]
    ydat = vel[x:y]
    
    deg = degrees[i]
    coeff = fitdata.calc_fit(xdat, ydat, degree = deg)
    distance += polynomial_integral(coeff,x,y)
#---------------------------------------
'''
    The 8 polynomial fit arrays calculated above are converted to functions
'''
def func1(t):
    return -2.78137660e+00 + 3.26608824e+00*t + 1.27316972e-01*(t**2) -9.82072915e-04*(t**3) -3.98006159e-05*(t**4) + 4.98752490e-07*(t**5)

def func2(t):
    return  2.46571667e+04 - 1.52146895e+03*t + 3.89244604e+01*(t**2) - 5.24449721e-01*(t**3) + 3.94073246e-03*(t**4) -1.56087892e-05*(t**5) +2.54690075e-08*(t**6)
        
def func3(t):
    return 1.74892624e+04 -3.42095706e+02*t + 2.31701990e+00*(t**2) - 4.88413265e-03*(t**3)

def func4(t):
    return -7.80638341e+04 + 1.74635131e+03*t  -1.51392956e+01*(t**2) + 6.54612342e-02*(t**3) -1.40821956e-04*(t**4) + 1.20766066e-07*(t**5)

def func5(t):
    return -4.33843182e+05 + 8.92677438e+03*t -7.61387548e+01*(t**2) + 3.46407751e-01*(t**3) -8.86192906e-04*(t**4) +1.20896931e-06*(t**5) -6.87087240e-10*(t**6)

def func6(t):
    return -4.39899733e+03 + 5.47764706e+01*t -1.42316779e-01*(t**2) + 1.56067801e-04*(t**3)

def func7(t):
    return -5.36096572e+06 + 7.28170551e+04*t -4.10837320e+02*(t**2) + 1.23282308e+00*(t**3) -2.07445199e-03*(t**4) +1.85541793e-06*(t**5) -6.88803760e-10*(t**6)

def func8(t):
    return -1.96165017e+08 + 1.96933865e+06*t -7.89937880e+03*(t**2) + 1.58247990e+01*(t**3) -1.58319792e-02*(t**4) + 6.32788008e-06*(t**5)

#---------------------------------------------------------------------
"""
    Each of the 8 functions are passed to gauss_quad to integrate it over the interval for the fit. The sum of these results yield the total 
distance travelled. 
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

degrees = np.array([5,6,3,5,6,3,6,5]) 


sum2 = 0.0
for i in range(0,int_count-1):
    min_num = int_bound[i]
    max_num = int_bound[i+1]

    x = int(min_num)
    y = int(max_num)
    
    if i == 0:
        sum2 += gauss_quad(func1,3,x,y)
        
    elif i == 1:
        sum2 += gauss_quad(func2,3,x,y)
   
    elif i == 2:
        sum2 += gauss_quad(func3,3,x,y)

    elif i == 3:
        sum2 += gauss_quad(func4,3,x,y)
      
    elif i == 4:
        sum2 += gauss_quad(func5,3,x,y)
      
    elif i == 5:
        sum2 += gauss_quad(func6,3,x,y)

    elif i == 6:
        sum2 += gauss_quad(func7,3,x,y)
    else:
        sum2 += gauss_quad(func8,3,x,y)


#-------------------
print("The total distance travelled according to the 'manual' integration:", distance,'\n')
print("The total distance travelled according to Gaussian quadrature:",sum2,'\n')
print("The 2 calculated values for total distance are nearly identical because" + "\n"+
      "both of the integration methods employed yield optimal results when"+"\n"+ "dealing with smooth polynomial functions.")

#---------------------------------
#1696024.3615013133
#1696286.9262007175
    
    
    
