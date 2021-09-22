# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:08:40 2020

@author: lesli
"""
import numpy as np
import random


""" These are the sampling functions"""

def dirac(t):
    '''dirac delta: constant'''
    return t

def normal(mu, sigma, low, high):
    
    '''
        random normal with mean `mu` and standard deviation 
        `sigma`, truncated below by `low` and above by `high` 
    '''
    condition = True
    count = 0
    while condition:
        count+=1
        if count == 1000:
            print("break is:",count)
            break
        t = np.random.normal(loc=mu, scale=sigma)
        if t >= low and t <= high:
            condition = False
        else:
            condition = True
        
    return t
     
def drive(miles, mu_mph, sigma_mph, low_mph, high_mph): 
    '''
        Converts distance and rate inputs to time in order to get a sample time
        
    '''
    
    mu_time = miles / (mu_mph/60)
    t_high = miles / (low_mph/60)
    t_low = miles / (high_mph/60)
    sigma_time = mu_time * (sigma_mph/mu_mph)
    
    t = normal(mu_time,sigma_time,t_low,t_high)
    return t
 
def light(t_cycle, t_green): 
    '''
        Calculates amount of wait time at traffic lights
    '''
    t_red = t_cycle - t_green
    rand =  random.random()
    tscale = 0 + (t_cycle-0)*rand
    t = 0.0 #wait time
    if tscale < t_red:
        t = t_red - tscale
    if tscale > t_red:
        t = 0.0
        
    return t

#----------------------------------------------

""" Simulation of commute"""
tcomm = np.zeros(100)
N = 100

for i in range(100):
    tsum = dirac(3) #step1
    tsum+= normal(0.5, 0.3 , 0.2, 4.0) #step2
    tsum+= drive(6, 30.0, 3.0, 5.0, 42.0) #step3
    tsum+=light(1.5, 0.5) #step4
    tsum+=drive(9, 45.0, 5.0, 35.0, 60.0) #step5
    tsum+= light(3.0, 0.5)#step 6
    tsum+=dirac(7) #step 7
    tcomm[i] = tsum
            
tcomm = np.sort(tcomm)

#----------------------------------------------
"""Percentile array for commute time is created"""

percentile = np.zeros(100)

for i in range(100):
    percentile[i] = 100.0 * ( i + 0.5 ) / N
    
#---------------------------------------
""" Computes maximum, 75th percentile, median, 25th percentile, and minimum commute times"""

maximum = tcomm[-1]
percent_75 = np.percentile(tcomm, 75)
median = np.percentile(tcomm, 50)
percent_25 = np.percentile(tcomm, 25)
minimum = tcomm[0]
#----------------------------------------------------
"""Compute a safe 95th percentile commute time"""
index = np.int( 0.95 * N)
estimate_95 = np.ceil(tcomm)
percent_95 = estimate_95[index]

#------------------------------

"""Plots cumulative distribution function of samples"""

Make_Plot = False  
if (Make_Plot):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tick
    fig = plt.figure(1)  
    
    fig, ax = plt.subplots()
    min_x = 30
    max_x = 45
    min_y = -5
    max_y = 105


    plt.plot(tcomm,percentile,'k', marker = "o") 
    ax.set_xlabel('Simulated Commute Time (min)',fontname='Courier New',fontsize=14)
    ax.set_ylabel('Percentile',fontname='Courier New',fontsize=14)

    #95th percentile horizontal line
    x_coordinates = [0, 44]
    y_coordinates = [index, index]


    x2_coordinates = [percent_95, percent_95]
    y2_coordinates = [-5, 105]

    plt.plot(x_coordinates, y_coordinates,'r')
    plt.plot(x2_coordinates, y2_coordinates,'b')

    ax = plt.gca()
    ax.xaxis.set_minor_locator(tick.MultipleLocator(.5))
    ax.yaxis.set_minor_locator(tick.MultipleLocator(5))



    textstr = '\n'.join((
            r'$\mathrm{Max}=%.2f$' % (maximum, ),
            r'$\mathrm{75th}=%.2f$' % (percent_75, ),
            r'$\mathrm{Median}=%.2f$' % (median, ),
            r'$\mathrm{25th}=%.2f$' % (percent_25, ),
            r'$\mathrm{Min}=%.2f$' % (minimum, )))

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='lavender', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.45, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='bottom', bbox=props)


    fig.suptitle('Commute Time Simulation ' + '| ' 
                 + 't_95% = ' + str(percent_95) ,fontname='Courier New',
                 fontsize=14) 
 

    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y) 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.tight_layout()
    fig.subplots_adjust(top=0.90)
    plt.grid(True)
    plt.show()
    fig.savefig('hw8_plot.png', dpi=300,bbox_inches='tight', edgecolor='none')






    
    
    
    
    







