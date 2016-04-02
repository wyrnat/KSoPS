'''
Created on 04.11.2015

@author: jannik
'''
from particleService import ParticleService
from interactionService import InteractionService
import numpy

class MeasureService(object):
    '''
    classdocs
    '''




    def getClusterParameter(self, cluster):
        """
        Returns array of the cluster parameter pos, r and rev
        """
        return [cluster.getX(), cluster.getY(), cluster.getR(), cluster.getREv()]
    
    
    def getMeanValues(self, clusterList):
        partServ = ParticleService()
        intServ = InteractionService()
        r = 0
        d = 0
        r_list = []
        d_list = []
        cluster_plist = []

        for cluster in clusterList.GET():
            # Radius
            r += cluster.getR()
            
            # Distance
            d_part = 0
            if len(cluster.getContacts()) != 0:
                for adCluster in cluster.getContacts():
                    if d_part > partServ.getParticleDistance(cluster, adCluster):
                        d_part = partServ.getParticleDistance(cluster, adCluster)
            else:
                d_part = intServ.findClosestCluster(cluster, clusterList)
            d += d_part
            
            # Radius List
            r_list.append(cluster.getR())
            
            # Distance List
            d_list.append(d_part)
            
            # Cluster Parameter List
            cluster_plist.append(self.getClusterParameter(cluster))
            
        return r/clusterList.clusterNumber() , d/clusterList.clusterNumber() , r_list , d_list, cluster_plist
                
    def getThickness(self, initval, clusterList):
        N = clusterList.getAllN()
        area = initval.getValue('area')
        r = initval.getValue('radius')
        
        thickness = 4 * numpy.sqrt(2) * N * r**3 / area**2
        return thickness  