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
        self.param = {'step_size': 1,               # simulation step size in ms
                      'measure_steps': 1,           #measuring after *n* steps ms 
                      'area': 200,                    #surface width in nm
                      'radius': 0.144,              #atom radius in nm
                      'bulk': 'fcc',
                      'lattice_const': 0.543,       #substrat lattice constant in nm
                      'T': 300,                     #Temperature in K
                      'growth_rate': 0.0000438,         #thickness growth rate in nm/ms
                      'flow_e': 0.6,                 #aggregation potential in eV
                      'diffusion_e': 0.5,           #diffusion potential in eV
                      'diffusion_exponent': -0.5,   #diffusion prop to N^de
                      'final_thickness': 10         #nm
                    }
        
        #set any parameter with initiation of object like inputparam = {'a':10}
        if inputparam != None:
            for value in inputparam:
                if value in self.param:
                    self.param[value] = inputparam[value]
        
        assert(self.param['step_size']>=1), "InitVals: step size is smaller than 1 (1ms is minimal step size)"
        assert(type(self.param['measure_steps']) == int), 'InitVals: measure_steps not of type (int)'
        assert(self.param['measure_steps'] >= 1), 'InitVals: measure_steps smaller than 1'
        assert(self.param['area'] > 0), 'InitVals: area is negative (unit is nm)'
        assert(self.param['radius'] > 0), 'InitVals: radius is negative (unit is nm)'
        assert(self.param['T'] > 0), 'InitVals: Temperature is negative (unit is Kelvin)'
        assert(self.param['growth_rate'] > 0), 'InitVals: growth_rate is negative (unit is nm/ms)'
        assert(self.param['flow_e'] > 0), 'InitVals: flow_e is negative'
        assert(self.param['diffusion_e'] > 0), 'InitVals: diffusion_e is negative'
        assert(self.param['final_thickness'] > self.param['growth_rate']), 'InitVals: final thickness smaller than growth rate'
        
    def getValue(self, bib):
        assert (bib in self.param), str(bib)+" not in initvals"
        return self.param[bib]