'''
Created on 10.12.2015

@author: jannik
'''
import numpy
from scipy import integrate

class CalculationService(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod        
    def dim2GaussFunction(radius_ev, radius, r_0):
        # diffusion length / sqrt(12)
        sigma = (radius_ev - radius)/3.464
        
        #round value to prevent overflow 
        if sigma < 0.001:
            #define a step function
            result = lambda y,x: (abs(numpy.sqrt(y**2+(x-r_0)**2)) < radius)*1.0
            return result
        else:
            c = numpy.sqrt(2*numpy.pi)
            
            #define the gauss function in 1dim. with 2dim normalisation
            dist = lambda r: numpy.exp(-(r/sigma)**2/2.) / c**2 / sigma**2
            
            #calculate the gauss with integration over the sphere
            dist_int = lambda r: (integrate.quad(dist, r-radius, r+radius))[0]
            
            result = lambda y,x: dist_int(numpy.sqrt(y**2+(x-r_0)**2))
        
            #returns a 2dim sphere integrated gauss function depending on y,x
            return result
        
        
        
    @staticmethod    
    def normalDistributionIntegration(radius_ev, radius, position):
        # diffusion length / sqrt(12)
        sigma = (radius_ev - radius)/3.464
        
        #round value to prevent overflow 
        if sigma < 0.001:
            return 1
        
        a = position - radius
        b = position + radius
        
        c = numpy.sqrt(2*numpy.pi)
        gauss = lambda x: numpy.exp(-(x/sigma)**2/2) / c / sigma
        result = integrate.quad(gauss, a, b)
        return result[0]
    
    @staticmethod
    def getCollisionProhability(radius_ev1, radius_ev2, radius1, radius2, distance):
        func1 = CalculationService.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = CalculationService.dim2GaussFunction(radius_ev2, radius2, distance)
        
        
        #If R_ev ~= R
        if func1(0,0) == func1(0,radius_ev1/2.):
            highfun = lambda x: numpy.sqrt(radius1**2-x**2)
            lowfun = lambda x: -highfun(x)
            prohability = integrate.dblquad(func2, -radius1, radius1,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
            return prohability[0]
        
        elif func2(0,0) == func2(0,radius_ev2/2.):
            highfun = lambda x: numpy.sqrt(radius2**2-(x-distance)**2)
            lowfun = lambda x: -highfun(x)
            prohability = integrate.dblquad(func1, distance-radius2, distance+radius2,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
            return prohability[0]
        
        else:
            #defines the overlap of both prohability functions
            overlap = lambda y,x: func1(y,x) * func2(y,x)
            
            x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
            x_diff = radius_ev1 - x
            y_diff = numpy.sqrt(radius_ev1**2-x**2)
            
            
            lowfun = lambda x: -y_diff
            highfun = lambda x: y_diff
        
            prohability = integrate.dblquad(overlap, x-x_diff, x+x_diff,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
        
            return prohability[0]
        
    def checkGreatProhability(self, radius_ev1, radius_ev2, radius1, radius2, distance, steps1, steps2):
        func1 = CalculationService.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = CalculationService.dim2GaussFunction(radius_ev2, radius2, distance)
        
        dim1Overlap = lambda x: func1(0,x) * func2(0,x)
        x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
        x_diff = radius_ev1 - x
        result = integrate.quad(dim1Overlap, x-x_diff, x+x_diff)
        if result >= 1:
            return True
        
        return False
        
        #TODO: Funktionen multiplizieren und eine line integration entlang x_diff
        