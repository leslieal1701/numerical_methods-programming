# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:48:52 2020

@author: lesli
"""
import numpy as np
np.seterr(all='raise')
from numpy import power
from math import factorial

def finite_diff(x, y):
    
    if x.size != y.size:
        raise ValueError("x and y must contain the same number of elements")
    
    N = y.size
    dydx = np.zeros(N)
    
    for i in range(1, N-1):
        try: dydx[i] = (y[i+1] - y[i-1])/(x[i+1] - x[i-1])  #central
        except FloatingPointError:
            print("x values must be unique")
            raise FloatingPointError
            
        
     
    dydx[0] = (y[1] - y[0])/(x[1] - x[0]) #forward
    
    
    dydx[-1] = (y[-1] - y[-2])/(x[-1] - x[-2]) #backward
     
            
    return dydx


def fd_formula(x, deriv=1):
    
    if type(deriv) != int:
        raise TypeError
        
    if deriv < 0:
        raise ValueError
    if deriv > x.size - 1:
        raise ValueError
    N = x.size    
    b = np.zeros(N)
    A = np.zeros([N,N])
    
    for i in range(N):
            for j in range(N):
                A[j,i] = power(x[i],j)
    b[deriv] = factorial(deriv)
                
    x = np.linalg.solve(A, b)
    
    return x

def polynomial_derivative(coef, x):
    
    if coef.size == 0:
        raise RuntimeError("Coefficient array doesn't contain any elements")
        
    if coef.size == 0 and coef[0] == 0:
        raise ValueError("Velocity function is zero")
    
    n = coef.size
    deriv = np.zeros(n)
    
    for i in range(n):
        deriv[i] = coef[i] * i
        
    p = deriv[-1]
    for i in range(n-2, 0, -1):
        p = deriv[i] + (x * p)
        
    return p
        
    


    
    

            
            