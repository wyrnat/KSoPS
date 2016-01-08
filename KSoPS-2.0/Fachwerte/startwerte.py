'''
Created on 19.10.2015

@author: jannik
'''
import numpy

class Startwerte(object):
    '''
    classdocs
    '''
    v = 10**10 #TODO besseren Wert finden
    k = 8.62 * 10**(-5)


    def __init__(self, inputparam = None):
        '''
        Constructor
        '''
        self.param = {'measure_steps': 50,      #measuring after *n* ms 
                      'area': 200,              #surface width in nm
                      'radius': 0.144,              #nm
                      'T': 273,                 #K
                      'lattice_const': 0.543,   #nm
                      'growth_rate': 0.2,
                      'schwoebl_e': 1,
                      'flow_e': 1,
                      'diffusion_e': 1,
                      'diffusion_choice': 0,    #prop. to 1/m 1/sqrt(m) or only adatom movement
                      'no_clustering': False,   #
                      'boarder_thickness': 10   #nm
                      
                      }
        if inputparam != None:
            #Schnittstelle fuer Einstellungen
            pass
        
    def getValue(self, bib):
        if bib in self.param:
            return self.param[bib]
        else:
            return None
            
        
    def getParticleRate(self):
        growth_rate = self.param['growth_rate']
        area = self.param['area']
        radius = self.param['radius']
        return int(numpy.ceil(3 * growth_rate * area**2 / (4 * numpy.pi * radius**3)))
        
    
    def getEventRadius(self):
        #TODO calculate Event radius out of Temperature and randomwalk test
        U = self.param['diffusion_e']
        T = self.param['T']
        a = self.param['lattice_const']
        
        # describes how many steps the atom can go
        steps = 4 * self.v * numpy.exp(-U / T / self.k)
        
        # describes the squared diffusion length
        diffusion_const = a**2 * steps
        
        # describes the distance the atom can go in a ms
        """
        IMPORTANT:
        The sigma in the gauss function for the particle distribution scales with 1/sqrt(12)
        That means, that 99.95% of the gauss function lies within the event radius
        """
        diff_length = numpy.sqrt(diffusion_const)
        
        return diff_length + self.param['radius']
            
            
    #def setValues(self, measure_steps = 50, area = 200, radius = 0.144, T = 273):