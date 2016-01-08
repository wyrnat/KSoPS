from Fachwerte.partikel import Partikel
from Fachwerte import startwerte
from Materialien import partikelList
from Services import partikelService
from Services.interaktionService import InteraktionService as intServ
#from Werkzeug import KSoPSWerkzeug




clusterList = partikelList.PartikelList()
adatomList = partikelList.PartikelList()
swerte = startwerte.Startwerte()

for i in range(1000):
    partikelService.PartikelService.createAdatom(swerte, clusterList)
    partikelService.PartikelService.createAdatom(swerte, adatomList)
    
    
print adatomList.GET()
    
r, rev = intServ.getSputterOverlap(adatomList, clusterList)
print r

for cluster in clusterList.GET():
    print cluster.getR()
#TODO print radius for test

    
