'''
Created on 15.10.2015

@author: jannik
'''

import numpy
import operator
from Fachwerte.particle import Particle

class ParticleList(object):
    '''
    classdocs
    '''


    def __init__(self, liste = []):
        '''
        Constructor
        '''
        self.Liste = list(liste)
        
    
    def clusterNumber(self):
        return len(self.Liste)    
        
    def getAllN(self):
        N = 0
        for particle in self.Liste:
            N += particle.getN()    
        return N
    
    def moveAll(self, dx, dy):
        for cluster in self.Liste:
            cluster.setX(cluster.getX() + dx)
            cluster.setY(cluster.getY() + dy)
    
    def getListforIndice(self, ind_list):
        mylist = []
        for i in ind_list:
            mylist.append(self.Liste[i])
        return mylist
            
            
    
    def getSameElements(self, liste):
        return [x for x in self.Liste if x in liste]   
    
    def removeParticle(self, particle):
        if particle in self.Liste:
            return self.Liste.pop(self.Liste.index(particle))  
        return None             
        
        
    def removeParticles(self, particle_list):
        """
        Removes particles from list
        @param particle_list: (list) particles to be removed
        """
        for i, particle in enumerate(self.Liste):
            if particle in particle_list:
                self.Liste.pop(i)
    
    
    def addParticle(self, par):
        """
        Add a particle object to the list
        @param par: (particle) The particle object to be added
        """
        assert (type(par) == Particle), 'given particle not from type "particle.Particle" '
        assert (par not in self.Liste), "particle is already in particle list"
        self.Liste.append(par)

                
    def sortList(self, attribute = 'N', reverse=True):
        # sort the list after the attribute beginning with 1=big, 0=small
        self.Liste.sort(key = operator.attrgetter(attribute), reverse = reverse)
        return self.Liste
        
    def list(self, mylist):
        """
        Wrapper for python lists
        """
        self.Liste = mylist
        
    def GET(self):
        """
        Dewrapper for python lists
        """
        return list(self.Liste)
    
    def numpyGET(self):
        return numpy.array(self.Liste[:])
        
        