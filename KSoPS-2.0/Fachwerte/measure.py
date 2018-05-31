'''
Created on 19.10.2015

@author: woehnert
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
        self.time = [0.0]
        self.thickness = [0.0]
        
        self.radius = [0.0]
        self.distance = [0.0]
        self.cluster_density = [0.0]
        self.r_list = [[0.0]]
        self.d_list = [[0.0]]
        
        self.dist_ww = [{'deposition_sputter': 0,
                       'clusterdeposition_sputter': 0,
                       'nucleation': 0,
                       'aggregation': 0,
                       'coalescence': 0
                       }]
        self.meancluster_properties = [[]]
        self.cluster_properties = [[]] # [x,y,r,rev]
        
    def save(self, time, thickness, radius, distance, cluster_density, r_list,
             d_list, dist_ww, cluster_plist):
        
        self.time.append(time)
        self.thickness.append(thickness)
        self.radius.append(radius)
        self.distance.append(distance)
        self.cluster_density.append(cluster_density)
        self.r_list.append(r_list)
        self.d_list.append(d_list)
        self.dist_ww.append(dist_ww)
        #self.meancluster_properties.append(meancluster_plist)
        self.cluster_properties.append(cluster_plist)
        
    def getThickness(self, index):
        return self.thickness[index]
    
        
    def getIndexWithThickness(self, thethickness):
        difference = abs(thethickness - numpy.array(self.thickness))
        min_diff = min(difference)
        result = difference.index(min_diff)
        return result
    
    def getMeanClusterProperties(self):
        return self.meancluster_properties
    
    def getClusterProperties(self):
        return self.cluster_properties
    
    
    
    
        
        
        
              
    
        