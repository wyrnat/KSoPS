'''
Created on 15.10.2015

@author: jannik
'''
import random
import numpy
from Fachwerte.partikel import Partikel
from Services.internService import InternService as intServ 

class PartikelList(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.Liste = []
        
        
    def getParticle(self, myhash):
        for cluster in self.Liste:
            if myhash == cluster.getHash():
                return cluster
        return None
    
    def removeParticles(self, hash_list):
        for i, cluster in enumerate(self.Liste):
            if cluster.getHash() in hash_list:
                return self.Liste.pop(i)
        return None
    
    
    def addParticle(self, par):
        assert (type(par) == Partikel), 'parameter not from type "partikel.Partikel" '
        self.Liste.append(par)
        
    def addToParticle(self, myhash, n):
        for cluster in self.Liste:
            if myhash == cluster.getHash():
                intServ.addAtoms(cluster, -1, n)
                
        
    def list(self, mylist):
        """
        Wrapper for python lists
        """
        self.Liste = mylist
        
    def GET(self):
        return self.Liste
        
        