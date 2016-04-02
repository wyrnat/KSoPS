'''
Created on 18.03.2016

@author: jannik
'''

from particleList import ParticleList

class PlList(object):
    '''
    Controls interacting particle Lists within a list
    '''


    def __init__(self, liste=[]):
        '''
        Constructor
        '''
        self.Liste = list(liste)
        
        
    def addAdatom(self, atom):
        self.Liste.append(ParticleList([atom]))
        
    def removePl(self, pl):
        """
        replace a particle list to be removed with empty particle list
        """
        if pl in self.Liste:
            self.Liste = [liste if liste!=pl else ParticleList() for liste in self.Liste]
        
    def removeCluster(self, cluster):
        """
        Search the cluster in all particle lists.
        If cluster number in particle list is zero after removal,
        set to entry to None
        """
        for liste in self.Liste:
            if liste.removeParticle(cluster) != None:
                if liste.clusterNumber() == 0:
                    print cluster
                    self.removePl(liste)
                return
            
    def findCluster(self, cluster):
        for liste in self.Liste:
            if cluster in liste.GET():
                return liste
        
        return None
            
        
    def clearList(self):
        clear_list = [liste for liste in self.Liste if liste.clusterNumber()==0]
        for clear in clear_list:
            self.Liste.remove(clear)
            
    def sortList(self):
        self.Liste.sort(key = lambda pl: pl.getInterN(), reverse=False)
        
    def GET(self):
        return list(self.Liste)
                