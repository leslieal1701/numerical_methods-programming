# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:32:50 2020

@author: lesli
"""
import ode
import numpy as np
from math import sqrt,pi,radians,sin


m= 500.0 #kg
b = 0.0 #damping coefficient [N.s/m] , b
k = 1.05e+06 #spring constant of cable [N/m]
g = 9.80665 #constant of gravitation [ m/s^2 ]
speed_c =  0.1 #cable speed [m/s]
W = m * g #Weight
tf = 1.0 #s
#--------------------------
w = sqrt(k/m) #angular frequency
frequency = w / (2*pi) #frequency)
#---------------------------

def crane_cable(state, t):
    '''Returns the ODE right-hand-side function for the crane cable mechanism seizure failure model

      Input: state[:,i] - 1D slice of state variables at i-th time step 
                      t - time at i-th time step

      Returns: dsdt[:,i] - 1D ODE rhs function evaluated at input state
      '''

    A = np.array([[0,1],[-k/m,-b/m]])
    dsdt = A @ state
    return dsdt     

tspan = np.array([0, tf])
y0 = np.array([0, speed_c])
num_steps = 100
solver = ode.RK4(crane_cable)
t, y = solver.solve_ivp(tspan,y0,num_steps)
load = y[0,:]
#------------------------------------  
"""Plots cumulative distribution function of samples"""

Make_Plot = False
if (Make_Plot):
    import matplotlib.pyplot as plt
    import matplotlib.ticker as tick
    fig = plt.figure(1)  
    
    fig, ax = plt.subplots()
    min_x = 0
    max_x = 1.0
    min_y = -.0025
    max_y = 0.0025


    plt.plot(t,load,'k', marker = "o") 
    ax.set_xlabel('Time (s)',fontname='Courier New',fontsize=14)
    ax.set_ylabel('Load Position (m)',fontname='Courier New',fontsize=14)


    ax = plt.gca()
    ax.xaxis.set_minor_locator(tick.MultipleLocator(.1))
    ax.yaxis.set_minor_locator(tick.MultipleLocator(.1))

    fig.suptitle('Load Position vs Time ',fontname='Courier New',fontsize=14) 
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y) 
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    fig.tight_layout()
    fig.subplots_adjust(top=0.90)
    plt.grid(True)
    plt.show()
    fig.savefig('hw9_plot.png', dpi=300,bbox_inches='tight', edgecolor='none')

#----------------------------------------------
cable_strength = 68.0 #[MPa]
safety_factor = 3.0
failure = (cable_strength / safety_factor) #22.7 
#--------------------
def calc_max_amp(load,t):
    ''' Returns the maximum amplitude given a load array and a time array.
    Calculates solution based on the equation: y(load) = A*sin(wt)'''
    
    n = t.shape[0]
    a0 = abs( load[1] / sin(radians(w*t[1])) )
    int_amp = 1
     
    for i in range(2,n):
        amp = load[i] / sin(radians(w*t[i]))
        if abs(amp) > a0:
            int_amp = i
            a0 = abs(amp)          
    max_amp = load[int_amp] / sin(w*t[int_amp])
    
    return abs(max_amp)


def calc_stress(diameter):
    ''' Calculates stress based on a given diameter'''
    return (4*max_tension) / (pi * diameter**2)


def gen_calc_dia(stress):
    ''' Returns diameter based on the formula: stress = tension / Area_of_cable '''
    return sqrt( (4*max_tension) / (pi*stress) )

def calc_min_diameter():
    ''' Finds the absolute minimum diameter that will yield the largest stress'''
    
    stress = np.linspace(0,22.7,228) #min and max stress in Mpa
    min_dia = gen_calc_dia(stress[1])
    int_dia = 1
    
    for st in range(2,stress.size):
        dia = sqrt( (4*max_tension) / (pi*st) )
        max_stress = calc_stress(dia)
        
        if dia < min_dia and max_stress > failure:
            int_dia = st
            min_dia = dia
            
    final_min_dia = gen_calc_dia(stress[int_dia])
    final_max_stress = (calc_stress(final_min_dia))         
        
            
    return final_min_dia, final_max_stress
    
            
max_amplitude = calc_max_amp(load,t)
max_tension = k *max_amplitude + W
diameter,max_stress = calc_min_diameter()

#print("Diameter:", diameter)
 #------------------------------

print("RESULTS ** ***** ***** ***** *****")
print(" frequency =", '{:6.2f}'.format(frequency) , "[Hz]")
print(" amplitude =", '{:6.2f}'.format(max_amplitude*1.0e3), "[mm]")
print(" tension =", '{:6.2f}'.format(max_tension/1.0e3) , "[kN]")
print(" stress =", '{:6.2f}'.format(max_stress) , "[MPa]")
#---------------------------------------------------------
#QUESTIONS:
''' 
A)I selected RK4 as my designated ODE solver because Forward Euler's method is 
    unconditionally unstable for un-damped oscillating systems.
    
B)I decided to use 100 time steps because this value produces a perfect sin wave in the plot.
    
    
C)I selected a cable strength of 68.0 MPa. Diameter of cable: 20.09 mm
    
D)The cable diameter undergoes very little change. This is due to the fact the load position only 
  varies drasrically after the first oscillation when using a new damping coefficient.
    
'''   
