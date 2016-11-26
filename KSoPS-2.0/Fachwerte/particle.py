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
    
    def getsurfaceN(self):
        return self.surfaceN
    
    """ Setter """
    
    def setX(self, x):
        self.x = x
    
    def setY(self, y):
        self.y = y
        
    def setR(self, r):
        self.r = r
        
    def setREv(self, rev):
        self.rev = rev 
        
    def setMaster (self, newmaster):
        self.master = newmaster
                
    def removeMaster(self, particle_list):
        self.master = None              
         
    def atomFlow(self, n):
        if self.N + n < 0:
            return False
        else:
            self.N += n
            return True
            
    def setSurfaceN(self, surfaceN):
        self.surfaceN = surfaceN
        

  