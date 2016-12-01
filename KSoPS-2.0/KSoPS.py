'''
Created on 25.11.2016

@author: jannik
'''

from Werkzeug.KSoPSWerkzeug import Werkzeug
from Services.ioService import IOService
from UI.pygameUI import PygameUI
import os

exp_name = "KSoPS_Test5"
if not os.path.exists('exp_name'):
    os.makedirs(exp_name)


myinitvals = {'step_size': 1,
              'measure_steps': 10,               #measuring after *n* ms 
              'area': 10,                      #surface width in nm
              'radius': 0.159,                  #atom radius in nm
              'bulk': 'fcc',
              'lattice_const': 0.543,           #substrat lattice constant in nm
              'T': 300,                         #Temperature in K
              'growth_rate': 0.0000438,         #thickness growth rate in nm/ms
              'flow_e': 0.5,                   #aggregation potential in eV
              'diffusion_e': 0.48,              #diffusion potential in eV
              'diffusion_exponent': -0.5,       #diffusion prop to N^de
              'final_thickness': 10             #nm
                    }

myWerkzeug = Werkzeug(myinitvals)
Measure = myWerkzeug.measure

#visualisation
screen = PygameUI(myWerkzeug.initVal, size = 700)

safeServ = IOService()

thickness = 0
counter = 0
ex = 'n'

while (thickness < myinitvals['final_thickness']) and (ex!="q"):
    mylist = myWerkzeug.run()

    thickness += myinitvals['growth_rate']
    print str(counter)+": "+str(thickness)+"  ("+str(mylist[-1])+"s)"
    #print list
    
    
    if (counter % myWerkzeug.initVal.getValue("measure_steps") == 0):
        safeServ.saveToTXT(Measure, exp_name+"/"+exp_name+"_params.txt")
        safeServ.saveEventsToTXT(Measure, exp_name+"/"+exp_name+"_events.txt")
        screen.draw(Measure.getClusterProperties(), -1)
        screen.safeImage(exp_name+"/"+exp_name, int(counter/myWerkzeug.initVal.getValue("measure_steps")))
    counter +=1
    #ex = input("quit?")
