'''A module for solving systems of ODEs that model initial value problems by implementing
explicit time-marching schemes within an object-oriented framework.'''

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 13:32:46 2020

@author: lesli
"""
import numpy as np

class ODESolver():
    ''' A base class for all time-marching methods  '''
    def __init__(self, func):
        ''' Initializes _func member based on the given function '''
        
        self._func = func
    
    def solve_ivp(self, tspan, y0, num_steps):
        '''Applies the forward Euler numerical method to solve the initial value problem.
            Solve_ivp takes in 3 parameters:
                
            -  tspan is a two element NumPy array holding tspan[0] = t0 and tspan[1]=tf .
            - y0 is a 1D NumPy array with as many elements as there are ODEs in the system of ODEs to be solved. 
            - num_steps is the number of time steps to use between t0 and tf .

        '''
        
        if tspan[0] > tspan[1] or num_steps < 1:
            raise ValueError
            
        N = num_steps
        dt = (tspan[1]-tspan[0]) / N
      
        t = np.linspace(tspan[0],tspan[1], N+1) 
        y = np.zeros([y0.size,t.size])
        
        y[:,0] = y0[:]
        for n in range(0, num_steps):
            y[:,n+1] = self.step(t[n], dt, y[:,n])
            
        
        return t,y
            
    def step(self, t_old, dt, y_old):
        '''  Returns an error because ODESolver is not meant to solve IVPs on its own  '''
        raise NotImplementedError
        
        
     
class ForwardEuler(ODESolver):
    '''A subclass of ODESolver that implements forward Euler '''
    
        
    def step(self, t_old, dt, y_old):
        ''' Returns the value y_n+1 as defined by the forward Euler numerical method. '''
        
        y = y_old + dt*self._func(y_old, t_old)
            
        return y
         
class RK4(ODESolver):
    ''' A subclass of ODESolver that implements the 4th-order Runge-Kutta method '''
    
    
    def step(self, t_old, dt, y_old):
        ''' Returns the value y_n+1 as defined by the classical 4th-order Runge-Kutta method.'''
    
        k1 = dt*self._func(y_old,t_old)
        k2 = dt*self._func(y_old + .5*k1,t_old + .5*dt)
        k3 = dt*self._func(y_old + .5*k2,t_old + .5*dt)
        k4 = dt*self._func(y_old + k3,t_old + dt)
        y = y_old + (1/6)*(k1+ 2*k2+ 2*k3 +k4)
            
        return y
    
    
    
#print(issubclass(RK4, ODESolver))
    