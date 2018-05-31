'''
Created on 16.03.2016

@author: woehnert
'''

import numpy
from random import random

v_e = 1e10 #Atomic potential frequency (in 1/ms)
k_b = 8.6173324 * 1e-5 # Boltzmann const. (in ev/K)

#lattice
scp = numpy.pi / 6.0
fcc = numpy.pi * numpy.sqrt(8) / 12.0
bcc = numpy.pi * numpy.sqrt(3) / 8.0
hcp = numpy.pi / numpy.sqrt(2) / 3.0

n_scp = 3
n_fcc = 6
n_bcc = 4
n_hcp = 6

lattice = {'scp': scp,
           'fcc': fcc,
           'bcc': bcc,
           'hcp': hcp
           }

n_coord = {'scp': n_scp,
           'fcc': n_fcc,
           'bcc': n_bcc,
           'hcp': n_hcp
           }

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
        bulk = initval.getValue('bulk')
        radius = initval.getValue('radius')
        step_size = initval.getValue('step_size')
        rndm = random()
        base = step_size*lattice[bulk]*growth_rate*area**2*3/(4*numpy.pi*radius**3)
        result = 1*(base % 1 > rndm) + int(base)
        return int(result)
    
    def getArrhenius(self, initval, potential):
        """
        calculates the arrhenius term without material system dependent factors
        """
        assert(type(potential)==float), 'Potential not of type float'
        assert(potential > 0), 'Potential is zero or negative'
        U = potential
        T = initval.getValue('T')
        step_size = initval.getValue('step_size')
        return step_size * v_e * numpy.exp(-U / k_b / T)
        
    
    def getAdatomEventRadius(self, initval):
        """
        calculate the eventradius of an adatom
        """
        
        a = initval.getValue('lattice_const')
        
        # describes how many steps the atom can go
        steps = self.getArrhenius(initval, initval.getValue('diffusion_e'))
        
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
    
    def getR(self, initval, n):
        assert(type(n)==int), 'getR: n not of type (Integer)'
        r = initval.getValue('radius')
        return numpy.power(2 * lattice[initval.getValue('bulk')] * n, 1/3.) * r
    
    def getSurfaceN(self, initval, R):
        r = initval.getValue('radius')
        n = int(numpy.ceil(lattice[initval.getValue('bulk')] * ( 3*(R/r)**2 - 6*R/r + 4)))
        return n
        
        
    def getAtomFlow(self, initval, surfaceN):
        """
        returns the atom number wandering from smaller to bigger cluster
        Only depending on surface atoms of smaller cluster
        """
        assert(type(surfaceN) == int), 'getAtomFlow: surfaceN type is not Integer'
        arrhenius = self.getArrhenius(initval, initval.getValue('flow_e')*n_coord[initval.getValue('bulk')] )
        floatflow = numpy.sqrt(surfaceN * arrhenius)
        #for flow is not a natural number
        flow = int(floatflow) + 1*((floatflow % 1)>random())
        return int(flow)
        
        
        
    