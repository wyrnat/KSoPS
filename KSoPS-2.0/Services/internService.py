'''
Created on 19.10.2015

@author: jannik
'''
import numpy

#const
sqrt3 = numpy.sqrt(3)

class InternService(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def setHoehe(self, R, partikel):
        n = partikel.getDistLen()
        h = n * R * sqrt3
        partikel.setVektorVal(h, 5)
        
    def setClusterRadius(self, R, partikel):
        atoms = partikel.getDist()[0]
        stacks = atoms / 6 + 1
        if atoms == 1:
            partikel.setR(R)
        elif (stacks % 2) == 0:
            partikel.setVektorVal(sqrt3 * R * stacks + R, 4)
        elif (stacks % 2) == 1:
            partikel.setVektorVal(R * numpy.sqrt(3*stacks**2 + 6*stacks + 1) + R)
        
    def PrecheckDist(self, partikel, pos):
        dist = partikel.getDist()
        if pos < 0:
            return False
        if len(dist) <= pos:
            return False
        if pos == 0:
            return True
        if dist[pos] + 1 <= (dist[pos-1]-1)/2:
            return True
        return False
        
    

        
    
    def addAtoms(self, partikel, pos, number=1):
        if pos < 0:
            pos = partikel.getDistLen() + pos
        for i in range(number):
            new_pos = pos    
            while self.PrecheckDist(partikel, new_pos) == False:
                new_pos -= 1
            n = partikel.getDist(new_pos)
            partikel.setDistVal(n+1, new_pos)
            
    def removeAtom(self, partikel, pos):
        partikel.setDistVal()
            
    def atomFlow(self, partikel, number):
        dist = partikel.getDist()
        n = partikel.getn()
        if number >= 0:
            dist[0] += number
        else:
            pass
                
            
        
            
        
            