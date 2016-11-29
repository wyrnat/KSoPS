'''
Created on 25.11.2016

@author: jannik
'''

from Werkzeug.KSoPSWerkzeug import Werkzeug
from Services.ioService import IOService


myinitvals = {'measure_steps': 1,               #measuring after *n* ms 
              'area': 200,                      #surface width in nm
              'radius': 0.144,                  #atom radius in nm
              'lattice_const': 0.543,           #substrat lattice constant in nm
              'T': 300,                         #Temperature in K
              'growth_rate': 0.0000438,         #thickness growth rate in nm/ms
              'flow_e': 0.55,                   #aggregation potential in eV
              'diffusion_e': 0.55,              #diffusion potential in eV
              'diffusion_exponent': -0.8,       #diffusion prop to N^de
              'final_thickness': 10             #nm
                    }

myWerkzeug = Werkzeug(myinitvals)
Measure = myWerkzeug.measure

safeServ = IOService()

thickness = 0
ex = 'n'

while (thickness < myinitvals['final_thickness']) and (ex!="q"):
    myWerkzeug.run()
    myWerkzeug.showSimulation(-1)
    safeServ.saveToTXT(Measure, "test.txt")
    thickness = myWerkzeug.measure.getThickness(-1)
    ex = input("quit?")
