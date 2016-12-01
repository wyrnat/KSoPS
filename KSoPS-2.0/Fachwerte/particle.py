'''
Created on 15.10.2015

@author: jannik
'''

import numpy
import math

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
        self.master = None
        self.surfaceN = 1       # Number of atoms on cluster surface
        self.N = 1
        
        
    """ Getter """
          
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def getR(self):
        return self.r
    
    def getREv(self):
        return self.rev
    
    def getMaster(self):
        return self.master
    
    def getN(self):
        return self.N
    
    def getSurfaceN(self):
        return self.surfaceN
    
    """ Setter """
    
    def setX(self, x):
        assert(not math.isnan(x)), 'setX: input is not a number'
        self.x = x
    
    def setY(self, y):
        assert(not math.isnan(y)), 'setY: input is not a number'
        self.y = y
        
    def setR(self, r):
        assert(not math.isnan(r)), 'setR: input is not a number'
        assert(r > 0), 'setR: r is negative'
        self.r = r
        
    def setREv(self, rev):
        assert(not math.isnan(rev)), 'setREv: input is not a number'
        assert(rev > 0), 'setREv: rev is negative'
        self.rev = rev 
        
    def setMaster (self, newmaster):
        assert (self != newmaster), 'setMaster: cluster will be its own master'
        assert (self != newmaster.getMaster()), 'setMaster: newMaster is also slave to this cluster'
        assert (self.N <= newmaster.getN()), 'setMaster: New Master is smaller than this cluster'
        self.master = newmaster
        
    def deleteMaster(self):
        assert(self.master != None), 'deleteMaster: Master is already (NoneType)'
        self.master = None       
         
    def atomFlow(self, n):
        assert (type(n)==int), "atomFlow: n is not Integer"
        assert (n > - self.N), 'atomFLow: number of remaining atoms negative'
        self.N += n
            
    def setSurfaceN(self, surfaceN):
        assert (type(surfaceN)==int), "setSurfaceN: surfaceN is not Integer"
        assert(surfaceN > 0), 'setSurfaceN: surfaceN is negative'
        self.surfaceN = surfaceN
        

  