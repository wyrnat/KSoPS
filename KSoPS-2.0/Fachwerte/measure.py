'''
Created on 19.10.2015

@author: jannik
'''
import numpy

class Measure(object):
    '''
    classdocs
    '''
    """
    TODO speichere nur die grundlegenden Werte,
    der Rest wird beim getter Aufruf berechnet
    """
    


    def __init__(self):
        '''
        Constructor
        '''
        self.thickness = []
        
        self.radius = []
        self.distance = []
        self.r_list = []
        self.d_list = []
        
        self.dist_ww = []
        self.cluster_properties = []
        
    def save(self, thickness, radius, distance, r_list,
             d_list, dist_ww, cluster_plist):
        
        
        self.thickness.append(thickness)
        self.radius.append(radius)
        self.distance.append(distance)
        self.r_list.append(r_list)
        self.d_list.append(d_list)
        self.dist_ww.append(dist_ww)
        self.cluster_properties.append(cluster_plist)
        
    def getThickness(self, index):
        return self.thickness[index]
    
    def getRadius(self, index):
        pass
        
    def getIndexWithThickness(self, thethickness):
        #if (thethickness < 0) or (thethickness > self.thickness[-1]):
        #    return None
        difference = abs(thethickness - numpy.array(self.thickness))
        min_diff = min(difference)
        result = difference.index(min_diff)
        return result
    
    
        
        
        
              
    
        