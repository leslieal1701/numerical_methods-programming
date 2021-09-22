""" A module to perform a least squares polynomial fit of data """


# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 22:27:53 2020

@author: lesli
"""
import numpy as np

def back_sub(U, b):
    
    """
    
        Computes the backward substitution given a 2D array and 1D array to solve an upper triangular matrix.
        
      
    
    """
    
    N = U.shape[0]
    x = np.zeros(N)
    
    for i in range(N-1, -1, -1):
        x[i] = b[i] 
        for j in range(i+1, N):
            x[i] -= U[i,j] * x[j]
        x[i] /= U[i,i]

    return x


def calc_fit(xdata, ydata, degree=1):
    """
        Returns a 1d NumPy array containing the coefficients that define the polynomial fitting function
        
        The procedure used to determine the coefficients relies upon the creation of a Vandermonde matrix;
        a matrix wwhose columns or rows are successive powers of an independent variable(xdata)
        
        After matrix A is created to fit the criteria for a Vandemonde matrix, the overdetermined system Ax=b
        where b = ydata  is solved using QR decomposition and backward substitution.
        
        Backward substitution will solve the upper triangular system created by the QR decomposition and return
        the 1D array, x, containing the polynomial coefficients.
    
    """
    
    assert degree >= 0, "The polynomial degree must be non‐negative"
    assert xdata.ndim == 1, "xdata must be a 1D array"
    assert xdata.size == ydata.size, "xdata and ydata must have the same number of elements"
    
    b = ydata.copy()
    m = xdata.size
    n = degree +1
  
    A = np.zeros([m,n])
    A[:,0] = 1
    
    row = A.shape[0]
    col = A.shape[1]
    
    
    deg = 0
    
    while deg < degree:
        for j in range(1,col):
            deg+=1
            for i in range(row):
                A[i,j] = xdata[i]**deg
                
                
    q, r = np.linalg.qr(A)
    Atb = q.T @ b
    x = back_sub(r,Atb)
    
    return x
    
    
    
def eval_fit(coeff, x):
    """ 
    
          Returns a 1D numpy array of a polynomial evaluated at positions specified by 1D array x. 
          
          Function takes the polynomial coefficients produced by calc_fit (coeff) and uses them to evaluate 
          the fitting polynomial at some given locations. 
          
     
    
    """
    
    N = x.size 
    C = coeff.size
    y = np.zeros([N])
    
    for i in range(N):
        y[i] = coeff[0]
        
        
    for i in range(N):
        for k in range(1,C):
            y[i]+= coeff[k]*(x[i]**k)
    
    return y



    
 
#test---------------------------------------------------    
#xdat = np.array([2.9,3.5,3.5,4.3])
#ydat = np.array([22.4,23.5,34.6,45.8])
#xval = np.array([2,4])

#coeff = calc_fit(xdat, ydat, degree=2)
#print(coeff)
    
#y = eval_fit(coeff,xval)

#print(y)
    