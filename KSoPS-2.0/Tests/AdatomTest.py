'''
Created on 21.03.2016

@author: jannik
'''

from Werkzeug import KSoPSWerkzeug

from Fachwerte.singleMeasure import SingleMeasure
from Fachwerte.initVals import InitVals
from Materialien.particleList import ParticleList

smeasure = SingleMeasure()
adatomList = ParticleList()
initval = InitVals()

w= KSoPSWerkzeug.Werkzeug()

w.sputter(adatomList)
print adatomList.clusterNumber()


                        