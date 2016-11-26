'''
Created on 04.11.2015

@author: jannik
'''

import numpy

class MeasureService(object):
    '''
    classdocs
    '''

    def getClusterParameter(self, cluster):
        """
        Returns array of the cluster parameter pos, r and rev
        """
        return [cluster.getX(), cluster.getY(), cluster.getR(), cluster.getREv(), cluster.getN()]
    
    
    def getMeanValues(self, clusterList, coalescenceList):
        r = 0
        d = 0
        r_list = []
        d_list = []
        cluster_plist = []

        for cluster in clusterList.GET():
            # Radius
            r += cluster.getR()
            
            # Distance
            d_part = self.findClosestCluster(cluster, clusterList, coalescenceList)
            d += d_part
            
            # Radius List
            r_list.append(cluster.getR())
            
            # Distance List
            d_list.append(d_part)
            
            # Cluster Parameter List
            cluster_plist.append(self.getClusterParameter(cluster))
            
        return r/clusterList.clusterNumber() , d/clusterList.clusterNumber() ,  r_list , d_list, cluster_plist
                
    def getThickness(self, initval, clusterList):
        N = clusterList.getAllN()
        area = initval.getValue('area')
        r = initval.getValue('radius')
        
        thickness = 4 * numpy.sqrt(2) * N * r**3 / area**2
        return thickness  
    
    def findClosestCluster(self, cluster, clusterList, coalescenceList):
        temp_liste = clusterList.GET()
        pl = coalescenceList.findCluster(cluster)
        temp_liste.removeParticles(pl)
        x_list = numpy.array([particle.getX() for particle in temp_liste])
        y_list = numpy.array([particle.getY() for particle in temp_liste])
        distance_list = numpy.sqrt( (cluster.getX()-x_list)**2 + (cluster.getY()-y_list)**2 )   
        return numpy.amin(distance_list)