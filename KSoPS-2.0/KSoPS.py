'''
Created on 25.11.2016

@author: jannik
'''

from Werkzeug.KSoPSWerkzeug import Werkzeug


myinitvals = {'measure_steps': 50,      #measuring after *n* ms 
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

myWerkzeug = Werkzeug(myinitvals)

thickness = 0

while (thickness < myWerkzeug.measure.getThickness(-1)):
    myWerkzeug.run()
    print myWerkzeug.measure.getThickness(-1)

