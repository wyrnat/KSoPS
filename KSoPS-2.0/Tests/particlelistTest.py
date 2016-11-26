'''
Created on 26.10.2016

@author: jannik
'''

from Materialien.particleList import ParticleList
from Fachwerte.initVals import InitVals
from Services.initValService import InitValService
from Services.particleService import ParticleService

initval = InitVals()
initServ = InitValService()
pServ = ParticleService()
adatomList = ParticleList()
for i in range(5):
    adatom = pServ.createAdatom(initval)
    adatomList.addParticle(adatom)

test = adatomList.GET()    
print adatomList.Liste
print test
print adatomList.Liste == test
test2 = test[:]
print adatomList.Liste == test2
adatomList.Liste.append(pServ.createAdatom(initval))
print adatomList.Liste
print test

# es wird eine neue Liste erzeugt bei der GET-Funktion, aber die Listen sind gleich

    
