'''
Created on 16.03.2016

@author: jannik
'''

import numpy

v_e = 1e10 #Atomic potential frequency (in 1/ms)
k_b = 8.6173324 * 1e-5 # Boltzmann const. (in ev/K)

class InitValService(object):
    '''
    classdocs
    '''
    
    def getParticleRate(self, initval):
        """
        returns number of deposited adatoms per simulation step
        """
        growth_rate = initval.getValue('growth_rate')
        area = initval.getValue('area')
        radius = initval.getValue('radius')
        return int(numpy.ceil(growth_rate * area**2 / (numpy.sqrt(32) * radius**3)))
    
    def getArrhenius(self, initval, potential):
        """
        calculates the arrhenius term without material system dependent factors
        """
        U = initval.getValue(potential)
        T = initval.getValue('T')
        return v_e * numpy.exp(-U / k_b / T)
        
    
    def getAdatomEventRadius(self, initval):
        """
        calculate the eventradius of an adatom
        """
        
        a = initval.getValue('lattice_const')
        
        # describes how many steps the atom can go
        steps = 3 * self.getArrhenius(initval, 'diffusion_e')
        
        # describes the squared diffusion length
        diffusion_const = a**2 * steps
        
        diff_length = numpy.sqrt(diffusion_const)
        
        return diff_length
    
    def getREv(self, initval, n):
        """
        Calculate the Eventradius for a cluster
        """
        potenz = initval.getValue('diffusion_exponent')
        arrhenius = self.getAdatomEventRadius(initval)
        
        return n**(potenz)*arrhenius
        
        
        
    def getAtomFlow(self, initval, R):
        """
        returns the atom number wandering from smaller to bigger cluster
        Only depending on surface atoms of smaller cluster
        """
        r = initval.getValue('radius')
        n = numpy.floor(numpy.pi / 3 / numpy.sqrt(2) * ( 6*(R/r)**2 - 12*R/r + 8))
        arrhenius = self.getArrhenius(initval, 'flow_e')
        return int(numpy.floor(n * arrhenius))
        
        
        
    