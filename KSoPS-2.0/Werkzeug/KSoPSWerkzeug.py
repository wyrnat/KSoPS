'''
Created on 15.10.2015

@author: jannik
'''
from Fachwerte import startwerte
from Materialien import partikelList

from Services.partikelService import PartikelService as pServ
from Services.interaktionService import InteraktionService as intServ

class Werkzeug(object):
    '''
    Regelt den Ablauf der Monte-Carlo Simulation
    '''


    def __init__(self, params):
        '''
        Initialisiert die Services und uebernimmt
        die GUI Parameter
        '''
        self.initVal = startwerte.Startwerte()
        self.adatomList = partikelList.PartikelList()
        self.particleList = partikelList.PartikelList()
        
    def run(self, step):
        
        #creates Adatoms and add them to adatomList
        self.sputter()
        
        #WW midair and hits on surface or clusters
        self.adatomHits()
        
        #calculate event radius hits for adatoms (bottom to top)
        self.eventRadiusHits()
        
        #move the rest, directly checking for collision
        self.move()
        
        #measures the actual state
        self.measure()
        
        
    def InterneProzesse(self):
        pass
    
    def sputter(self):
        #number of particles per ms to reach sputter rate
        noa = self.initVal.getParticleRate()
        for i in range(len(noa)):
            #adding new particles to adatomList
            pServ.createAdatom(self.initVal, self.adatomList)
            
    def adatomHits(self):
        
        #lists of hash values of clusters from partikelList
        r_hits, rev_hits = intServ.getSputterOverlap(self.adatomList, self.particleList)
        
        for myhash_list in r_hits:
            self.particleList.addToParticle(myhash_list[0], 1)
        self.adatomList.removeParticles(r_hits)
        
        for myhash in rev_hits:
            # fast calculation, if the prohability is cleary over 1
            if intServ.checkGreatProhability() == True:
                self.particleList.addToParticle(myhash[0], 1)
                self.adatomList.removeParticles(rev_hits)
            else:
                #TODO: Funktionen aus dem CalculationService nach interaktionServive kopieren
                
            
            
    
    def Clusterbewegung(self):
        pass
    
    def Messung(self):
        pass
    
    def InterclusterFluss(self):
        pass
    
    def Kollisionen(self):
        pass
        