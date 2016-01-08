'''
Created on 15.10.2015

@author: jannik
'''

import numpy

class Partikel(object):
    '''
    classdocs
    '''
    testfunc = lambda x: x


    def __init__(self, x, y, r, rev, vn, parent, angle, dist): #, prob_func):
        '''
        Constructor
        '''
        self.vektor = [x,y,r,rev,vn]
        self.myhash = 0
        self.parent = parent
        self.angle = angle
        self.dist = dist
        #self.prob_func = prob_func
        
        
    """ Getter """
        
        
    def getX(self):
        return self.vektor[0]
        
    def getY(self):
        return self.vektor[1]
        
    
    def getR(self):
        return self.vektor[2]
    
    def getREv(self):
        return self.vektor[3]
    
    def getVN(self):
        return self.vektor[4]
        
    def getHash(self):
        return self.myhash
    
    def getParent(self):
        return self.parent
    
    def getAngle(self):
        return self.angle
    
    def getAngleAsVector(self):
        return numpy.cos(self.angle) , numpy.sin(self.angle)
    
    def getDist(self, pos = None):
        if pos == None:
            return self.dist
        elif pos in  range(len(self.dist)):
            return self.dist[pos]
        else:
            return False
        
    
    def getDistLen(self):
        return len(self.dist)
    
#     def getProbFunc(self):
#         return self.prob_func
    
    """ Setter """
    
    def setPos(self, array):
        if type(array) == numpy.ndarray:
            self.vektor =array
            return True
        else:
            try:
                self.vektor = numpy.array(array)
            except:
                return False
            return True

        
    def setPosVal(self, value, pos):
        if pos in [0,1]:
            self.vektor[pos] = value
            
        
    def setR(self, r):
        self.Vektor[2] = r
        
    def setREv(self, rev):
        self.vektor[3] = rev  
        
    def setVN(self, vn):
        self.vektor[4] = vn      
    
    def setHash(self, myhash):
        self.myhash = myhash
        
    def setParent(self, parent):
        self.parent = parent
        
    def setAngle(self, angle):
        self.angle = angle % (2 * numpy.pi)
        
    def setDist(self, value):
        self.dist = value
        
    def setDistVal(self, value, pos):
        assert (value >= 0), 'setDistVal: value negative'
        assert (len(self.dist) > pos), 'setDistVal: pos out of range'
        if pos in range(len(self.dist)):
            self.dist[pos] = value
        
        if self.dist[-1] != 0:
            self.dist.append(0)
            
#     def setProbFunc(self, func):
#         if type(func) == type(self.testfunc):
#             self.prob_func = func
#             return True
#         else:
#             return False
#             
    
    