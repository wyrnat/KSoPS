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
        self.param = {'measure_steps': 50,      #measuring after *n* ms 
                      'area': 10,              #surface width in nm
                      'radius': 0.144,              #nm
                      'T': 273,                 #K
                      'lattice_const': 0.543,   #nm
                      'growth_rate': 0.01,
                      'schwoebl_e': 1,
                      'flow_e': 1,
                      'diffusion_e': 1,
                      'diffusion_choice': 'pot',    #prop. to 1/m 1/sqrt(m) or only adatom movement
                      'no_clustering': False,   #adatoms clustering 2dim on surface
                      'border_thickness': 10   #nm
                      
                      }
        if inputparam != None:
            for value in inputparam:
                if value in self.param:
                    self.param[value] = inputparam[value]
        
    def getValue(self, bib):
        if bib in self.param:
            return self.param[bib]
        else:
            return None
            
            
    #def setValues(self, measure_steps = 50, area = 200, radius = 0.144, T = 273):