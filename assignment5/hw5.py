# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:24:34 2020

@author: lesli
"""

import numpy as np
from find_root import bisection
import matplotlib.pyplot as plt


R = 0.08205 #universal gas constant
def bb_residual(P, T, V, A0, B0, a, b, c):
    
  
    beta = R*T*B0-A0-((R*c)/T**2)
    gamma = -R*T*B0*b+(A0*a)-((R*B0*c)/T**2)
    delta = (R*B0*b*c)/T**2
    
    val1 = (R*T)/V
    val2 = beta/V**2
    val3 = gamma/V**3
    val4 = delta/V**4

     
    residual = P - val1 - val2 - val3 - val4
    
    
    return residual


#---------------------------------------------------------------------    
    

A0 = 2.27690
B0 = 0.05587
a = 0.01855 
b = -0.01587
c = 1.28300e5

T1 = 0 + 273
T2 = 200 + 273
pressure = np.zeros(200)
for i in range(200):
    pressure[i] = i+1

Z = np.zeros([200, 2])
    
vlow = 0.01
vupp = 100
plt.figure(1, figsize=(8,6))


for j in range(200):
    V =  bisection(lambda V: bb_residual(pressure[j], T1, V, A0, B0, a, b, c), vlow, vupp)
    Z[j,1] = (pressure[j]*V) / (R*T1)
    Z[j,0] = j+1
plt.plot(pressure,Z[:,1], 'b', label = 'T=0°C')   

for k in range(200):
    V =  bisection(lambda V: bb_residual(pressure[k], T2, V, A0, B0, a, b, c), vlow, vupp)
    Z[k,1] = (pressure[k]*V) / (R*T2)
plt.plot(pressure,Z[:,1],'r', label = 'T=200°C') 



plt.title('Aleman, Leslie (alemal2)')
# label the x- and y-axes
plt.xlabel('Pressure (atm) ', fontsize=14)
plt.ylabel('Compressibility Factor (Z)', fontsize=14)
plt.legend(fontsize=14, loc=4) # add a legend
plt.gca().grid()
plt.savefig('hw5_plot.png', dpi=300, edgecolor='none')


    
    
    