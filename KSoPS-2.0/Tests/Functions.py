'''
Created on 26.11.2016

@author: woehnert
'''

import numpy

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def dim2GaussFunction(self, radius_ev, radius, r_0):
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
        
        
            
    def normalDistributionIntegration(self, radius_ev, radius, position):
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
    

    def getCollisionProhability(self, cluster1, cluster2):
        radius1 = cluster1.getR()
        radius2 = cluster2.getR()
        radius_ev1 = cluster1.getREv()
        radius_ev2 = cluster2.getREv()
        distance = numpy.sqrt( (cluster1.getX()-cluster2.getX())**2 + (cluster1.getY()-cluster2.getY())**2 )
        func1 = self.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = self.dim2GaussFunction(radius_ev2, radius2, distance)
        
        
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
            
            center = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
            
            x_diff = radius_ev1 - center
            if (radius_ev1**2-center**2 < 0):
                print "sqrt error: ", (radius_ev1**2-center**2)
            y_diff = numpy.sqrt(abs(radius_ev1**2-center**2))
            
            
            lowfun = lambda x: -y_diff
            highfun = lambda x: y_diff
        
            prohability = integrate.dblquad(overlap, center-x_diff, center+x_diff,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
        
            return prohability[0]
        
    def checkGreatProhability(self, cluster1, cluster2):
        """
        estimate if the overlap integral of the prohability density functions of two clusters
        is greater than 1 to shorten calculation time.
        Make a cut along the centers of the event radii and integrate it
        """
        radius1 = cluster1.getR()
        radius2 = cluster2.getR()
        radius_ev1 = cluster1.getREv()
        radius_ev2 = cluster2.getREv()
        distance = numpy.sqrt( (cluster1.getX()-cluster2.getX())**2 + (cluster1.getY()-cluster2.getY())**2 )
        
        func1 = self.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = self.dim2GaussFunction(radius_ev2, radius2, distance)
        
        dim1Overlap = lambda x: func1(0,x) * func2(0,x)
        
        #overlap cross section of event radii
        x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
        x_diff = radius_ev1 - x
        result = integrate.quad(dim1Overlap, x-x_diff, x+x_diff, epsabs=0.01, epsrel=0.01)
        return result[0]