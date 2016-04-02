from Fachwerte.particle import Partikel
from Fachwerte import initVals
from Materialien import particleList
from Services import particleService
from Services.interactionService import InteraktionService as intServ
#from Werkzeug import KSoPSWerkzeug




clusterList = particleList.PartikelList()
adatomList = particleList.PartikelList()
swerte = initVals.Startwerte()

for i in range(1000):
    particleService.PartikelService.createAdatom(swerte, clusterList)
    particleService.PartikelService.createAdatom(swerte, adatomList)
    
    
print adatomList.GET()
    
r, rev = intServ.getSputterOverlap(adatomList, clusterList)
print r

for cluster in clusterList.GET():
    print cluster.getR()
#TODO print radius for test

    
