'''
Created on 25.11.2016

@author: jannik
'''

import numpy
import scipy
from Werkzeug.KSoPSWerkzeug import Werkzeug
from Services.ioService import IOService
from UI.pygameUI import PygameUI
import os

exp_name = "300K_new"
if not os.path.exists("Simulationen/"+exp_name):
    os.makedirs("Simulationen/"+exp_name)


myinitvals = {'step_size': 1,
              'measure_steps': 50,               #measuring after *n* ms 
              'area': 100,                      #surface width in nm
              'radius': 0.159,                  #atom radius in nm
              'bulk': 'fcc',
              'lattice_const': 0.543,           #substrat lattice constant in nm
              'T': 300,                         #Temperature in K
              'growth_rate': 0.0000438,         #thickness growth rate in nm/ms
              'flow_e': 0.1,                   #bulk potential in eV (bond per coordinate number
              'diffusion_e': 0.48,              #substrat potential in eV
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

    thickness += myinitvals['growth_rate']*myinitvals['step_size']
    print str(counter)+": "+str(thickness)+"  ("+str(mylist[-1])+"s)"
    #print list
    
    
    if (counter % myWerkzeug.initVal.getValue("measure_steps") == 0):
        safeServ.saveToTXT(Measure, "Simulationen/"+exp_name+"/"+exp_name+"_params.txt")
        safeServ.saveEventsToTXT(Measure, "Simulationen/"+exp_name+"/"+exp_name+"_events.txt")
        screen.draw(Measure.getClusterProperties(), Measure.time[-1], Measure.thickness[-1], -1)
        screen.safeImage("Simulationen/"+exp_name+"/"+exp_name, int(counter/myWerkzeug.initVal.getValue("measure_steps")))
    counter +=1
    #ex = input("quit?")
