'''
Created on 19.10.2015

@author: jannik
'''
import numpy

class InitVals(object):
    '''
    classdocs
    '''


    def __init__(self, inputparam = None):
        '''
        Constructor
        '''
        self.param = {'measure_steps': 1,      #measuring after *n* ms 
                      'area': 5,              #surface width in nm
                      'radius': 0.144,              #nm
                      'T': 273,                 #K
                      'lattice_const': 0.543,   #nm
                      'growth_rate': 0.005,     #nm/ms
                      'flow_e': 10,
                      'diffusion_e': 0.6,
                      'diffusion_exponent': -0.8,    #diffusion prop to N^de
                      'no_clustering': False,   #adatoms clustering 2dim on surface
                      'final_thickness': 10   #nm
                    }
        
        #set any parameter with initiation of object like inputparam = {'a':10}
        if inputparam != None:
            for value in inputparam:
                if value in self.param:
                    self.param[value] = inputparam[value]
        
    def getValue(self, bib):
        assert (bib in self.param), "value not in initvals"
        return self.param[bib]