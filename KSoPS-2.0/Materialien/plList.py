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
        """
        create new particleList with one adatom
        """
        self.Liste.append(ParticleList([atom]))
        
    def removePl(self, pl, empty = False):
        """
        replace a particle list to be removed with empty particle list
        """
        assert (pl in self.Liste), "removepl: particleList not in coalescenceList"    
        if pl in self.Liste:
            i = self.Liste.index(pl)
            self.Liste[i] = ParticleList()
        assert (pl not in self.Liste), "removepl: particleList still in coalescenceList"
        
        
    def removeCluster(self, cluster):
        """
        Search the cluster in all particle lists.
        If cluster number in particle list is zero after removal,
        set to entry to None
        """
     
        for liste in self.Liste:
            if liste.removeParticle(cluster) != None:
                if liste.clusterNumber() == 0:
                    self.removePl(liste)
                return
            
    def findCluster(self, cluster):
        """
        Returns the list in which the particle is stored
        """
        for liste in self.Liste:
            if cluster in liste.GET():
                return liste
        
        return None
    
    def getListbyIndex(self, index):
        return self.Liste[index]
        
    def clearList(self):
        clear_list = [liste for liste in self.Liste if liste.clusterNumber()==0]
        for clear in clear_list:
            self.Liste.remove(clear)
            
    def sortList(self, bigfirst=True):
        """
        Sorts Liste starting the particlelist with most atoms
        """
        self.Liste.sort(key = lambda pl: pl.getAllN, reverse=bigfirst)
        if len(self.Liste)>=2:
            assert(self.Liste[0].getAllN()>=self.Liste[1].getAllN())
        
    def GET(self):
        return list(self.Liste)
                