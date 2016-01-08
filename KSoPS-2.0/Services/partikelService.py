'''
Created on 15.10.2015

@author: jannik
'''

import random
from Fachwerte.partikel import Partikel
from internService import InternService

class PartikelService(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod    
    def createAdatom(inputVal, adatomList):
        """
        Erzeugt ein Adatom und
        fuegt es zur Liste hinzu
        """
        assert(inputVal.getValue('area') > 0), 'erzeugeAdatome: Area zu klein'
        assert(inputVal.getValue('radius') > 0), 'erzeugeAdatome: Radius zu klein'
        
        x = (random.random() - 0.5) * inputVal.getValue('area')
        y = (random.random() - 0.5) * inputVal.getValue('area')
        r = inputVal.getValue('radius')
        rev = inputVal.getEventRadius()
        parent = None       # hash Wert des Master Clusters
        angle = 0           # 0 bis 2 pi
        vn = 1
        dist = [1]
        
        adatom = Partikel(x,y,r,rev,vn,parent,angle, dist)
        
        adatom.setHash(hash(adatom))
        
        adatomList.addParticle(adatom)
    
    @staticmethod    
    def AdatomOnSurface(myhash, adatomList, clusterList):
        p = adatomList.removePartikel(myhash)
        if p != None:
            clusterList.addPartikel(p)
        
    @staticmethod    
    def AdatomOnCluster(myhash, adatomList, cluster, latestMeasure):
        p = adatomList.removePartikel(myhash)
        InternService.addAtoms(cluster, -1)
        
        
        
        
        
        
        
        
        