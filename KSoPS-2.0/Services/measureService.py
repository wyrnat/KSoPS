'''
Created on 04.11.2015

@author: jannik
'''

import numpy
from Fachwerte.particle import Particle
from Materialien.particleList import ParticleList
from Services.particleService import ParticleService

class MeasureService(object):
    '''
    classdocs
    '''
    
    
    def getMeanValues(self, initval, clusterList, coalescenceList):
        r = 0
        d = 0
        r_list = []
        d_list = []
        #meancluster_plist = []
        
        #REPRESENTATIVELIST
        #representiveList = self.getRepresentingCluster(initval, coalescenceList)

        for cluster in clusterList.GET():
            # Radius
            r += cluster.getR()
            
            # Distance
            d_part = self.findClosestCluster(cluster, clusterList)
            d += d_part
            
            # Radius List
            r_list.append(cluster.getR())
            
            # Distance List
            d_list.append(d_part)
            
            # Cluster Parameter List (REPRESENTAVIELIST)
            #meancluster_plist.append(self.getClusterParameter(cluster))
        
        meanR = r/clusterList.clusterNumber()
        meanD = d/clusterList.clusterNumber()
        CDensity = clusterList.clusterNumber()/(1.0*initval.getValue('area')**2)*10**6   #cluster/micrometer**2

        return meanR , meanD , CDensity ,  r_list , d_list #, meancluster_plist
    
    def getclusterPropList(self, clusterList):
        cluster_plist = []
        for cluster in clusterList.GET():
            cluster_plist.append(self.getClusterParameter(cluster))
        return cluster_plist
            
    
    def getRepresentingCluster(self, initval, coalescencelist):
        partServ = ParticleService()
        representiveList = ParticleList()
        
        for pl in coalescencelist.GET():
            x, y = pl.getMeanPosition()
            par = Particle(x,y,r=1,rev=1)
            par.atomFlow(pl.getAllN()-1)
            partServ.setClusterR(initval, par)
            partServ.setClusterRev(initval, par, par.getN())
            
            representiveList.addParticle(par)
        return representiveList
        
                
    def getTimeThickness(self, initval, simulation_step):
        thickness = simulation_step * initval.getValue('growth_rate')
        time = simulation_step * initval.getValue('step_size') / 1000.0
        return time, thickness  
    
    def findClosestCluster(self, cluster, clusterList):
        temp_liste = clusterList.GET()
        temp_liste.pop(temp_liste.index(cluster))
        x_list = numpy.array([particle.getX() for particle in temp_liste])
        y_list = numpy.array([particle.getY() for particle in temp_liste])
        distance_list = numpy.sqrt( (cluster.getX()-x_list)**2 + (cluster.getY()-y_list)**2 )
        if len(distance_list) == 0:
            return 0
        else:   
            return numpy.amin(distance_list)
    
    def getClusterParameter(self, cluster):
        """
        Returns array of the cluster parameter pos, r and rev
        """
        
        masterN = 0
        # check if cluster has a master
        if cluster.getMaster() != None:
            masterN = cluster.getMaster().getN()
        return [cluster.getX(), cluster.getY(), cluster.getR(), cluster.getREv(), cluster.getN(), masterN]