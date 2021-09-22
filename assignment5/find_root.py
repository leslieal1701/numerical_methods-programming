""" A module for finding the roots of a function """



# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:24:46 2020

@author: lesli
"""

def bisection(func, xlow, xupp, ftol=1e-12, xtol=1e-7,maxiter=100):
    """
    
        Returns the root of a function by implementing the bisection method.
        
        Given an interval [xlow, xupp] and a function func, the bisection method will return x such that f (x) ≈ 0.
        The bisection method begins by dividing the interval [xlow, xupp] in half and evaluating the function at the midpoint, xmid,
        and then evaluating the function at the midpoint: f(xmid)
        
        Now that we now have two intervals, [xlow, xmid] and [xmid, xupp], we select an interval depending on the value of f(xlow)*f(xmid)
        There are 3 possibilities:  
        1. If f(xlow)*f(xmid) < 0, then there is a root in [xlow, xmid].
        2. If f(xlow)*f(xmid) > 0, then there is a root in [xmid, xupp].
        3. If f(xlow)*f(xmid) = 0, then f(xmid) = 0
        
        Once we choose one of the two intervals, the bisection method iterates until one of the following conditions is met:
         1. the function magnitude is below ftol
         2. the bracket size xupp ‐ xlow is less than xtol
         3. the maximum number of iterations, maxiter, has been reached
            
    
    """
    assert xupp > xlow, "Upper boundary must be greater than lower boundary"
    assert func(xlow) != 0.0 or func(xupp) != 0.0, "An exact root cannot be provided as either xlow or xupp"
    assert func(xupp)*func(xlow) < 0, "Values of xlow and xupp that bracket the root must be provided"
    assert maxiter >= 1 and maxiter <= 1000, " Maxiter cannot be set to something less than 1 or greater than 1,000"
    
    
    f_i = func(xlow)
    f_u = func(xupp)
    xmid = (1/2)*(xlow+xupp)
    f_mid = func(xmid)
    
    
    count = 0
    
    while abs(f_mid) > ftol and abs(xupp-xlow) > xtol and count < maxiter:
        count+=1
        
        if (f_i*f_mid) < 0.0:
            xupp = xmid
            f_u = func(xupp)
            f_mid = f_u
        elif (f_i*f_mid) > 0.0:
            xlow = xmid
            f_i = func(xlow)
            f_mid = f_i
        elif (f_i*f_mid) == 0.0:
            break
            
        xmid = (1/2)*(xlow+xupp)
        f_mid = func(xmid)
            
        
    return xmid
            
        
        
        
    
