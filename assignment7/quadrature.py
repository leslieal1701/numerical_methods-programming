""" A module for approximating an integral using the midpoint rule, trapezoidal rule, and gaussian quadrature"""


# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:22:03 2020

@author: lesli
"""

import numpy as np

def midpoint(fvals, dx):
    """
        Returns the midpoint-rule approximation to an integral based on the values in the 1D array fvals.
         The parameter dx denotes x, the interval size.
    
    """
    
    if dx <= 0:
        raise ValueError
    
    n = fvals.size
    sum = 0.0
    for i in range(n):
        sum+= fvals[i] * dx
        
    return sum


def trapezoidal(fvals, dx):
    """
        Returns the trapezoidal-rule approximation to an integral based on the values in the 1D array fvals.
         The parameter dx denotes x, the interval size.
    """
    if dx <= 0:
        raise ValueError
        
    n = fvals.size
    sum = (dx/2)*(fvals[0]+fvals[-1])
    for i in range(1,n-1):
        sum+= fvals[i] * dx
        
    return sum 

def gauss_quad(func, numpts, a=-1, b=1):
    
   ''' Gauss-Legendre quadrature of function over [a,b]

    Integrates user provided `func` over the interval [a,b] using
    Gauss-Legendre quadrature with `numpts` nodes for function
    evaluations.  Only 1 <= numpts <= 3 is supported.
    
    Input:  func   -- function to integrate
            numpts -- number of nodes
            a      -- lower bound of integral
            b      -- upper bound of integral
    '''
   if a > b:
        raise ValueError
        
    
   if numpts == 1:
       xpts = np.array([0.0])
       wgts = np.array([2.0])
   elif numpts == 2:
       xpts = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
       wgts = np.array([1.0, 1.0])
   elif numpts == 3:
       xpts = np.array([0,-np.sqrt(3/5),np.sqrt(3/5)])
       wgts = np.array([8/9, 5/9,5/9])
   else:
       raise ValueError
        
   c1 = (b-a)/2
    
    # apply quadrature formula
   integral = 0.0
   for i in range(numpts):
       c0 = a + (((xpts[i] + 1)/2) * (b-a))
       integral += wgts[i] * func(c0)
    
   return c1* integral

        
        