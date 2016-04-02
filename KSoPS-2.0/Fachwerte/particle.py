'''
Created on 15.10.2015

@author: jannik
'''

import numpy

class Particle(object):
    '''
    classdocs
    '''

    def __init__(self, x, y, r, rev):
        '''
        Constructor
        '''
        self.x = x
        self.y = y
        self.r = r
        self.rev = rev
        self.contacts = []
        self.interN = 1         # Number of atoms with border to substrate
        self.surfaceN = 1       # Number of atoms on cluster surface
        self.dist = [1,0]
        
        
    """ Getter """
          
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def getR(self):
        return self.r
    
    def getREv(self):
        return self.rev
    
    def getContacts(self):
        return self.contacts
    
    def getN(self):
        return self.dist[0]
    
    def getInterN(self):
        return self.interN
    
    def getDist(self, pos = None):
        if pos == None:
            return self.dist
        elif pos in  range(len(self.dist)):
            return self.dist[pos]
        else:
            return False
        
    def getDistLen(self):
        return len(self.dist)
    
    """ Setter """
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
        
    def setR(self, r):
        self.r = r
        
    def setREv(self, rev):
        self.rev = rev
        
    def addContacts(self, particle_list):
        for particle in particle_list:
            if particle not in particle_list:
                self.contacts.append(particle)   
                
    def removeContacts(self, particle_list):
        for i, particle in enumerate(particle_list):
            if particle in self.contacts:
                self.contacts.pop(i)               
        
        
    def atomFlow(self, n):
        if self.dist[0] + n < 0:
            return False
        else:
            self.dist[0] += n
            
    def setInterN(self, interN):
        self.interN = interN
        
    def setSurfaceN(self, surfaceN):
        self.surfaceN = surfaceN
        
    def setDist(self, value):
        self.dist = value
        
    def setDistVal(self, value, pos):
        assert (value >= 0), 'setDistVal: value negative'
        assert (len(self.dist) > pos), 'setDistVal: pos out of range'
        if pos in range(len(self.dist)):
            self.dist[pos] = value
        
        if self.dist[-1] != 0:
            self.dist.append(0)
  