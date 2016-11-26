'''
Created on 19.10.2015

@author: jannik
'''
import numpy
from scipy import integrate
from particleService import ParticleService
from random import random
from setuptools.command.build_ext import if_dl

class InteractionService(object):
    '''
    classdocs
    '''

        
    def adatomOnCluster(self, initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure):
        """
        Checks for overlapping radii of clusters and sputtered atoms
        If overlap, delete the sputtered atom and increase the atom Number of the cluster by 1
        else, remove the sputtered atom from the adatomList and add it to clusterList, adatomWWList and coalescenceList
        @param initval: (Initvals) class containing the system initial values
        @param adatomList: (ParticleList) Class with fresh sputtered atoms
        @param adatomWWList: (ParticleList) Class with all adatoms deposited on the surface
        @param clusterList: (ParticleList) class contains all clusters
        @param coalescenceList: (PlList) class containing ParticleLists of merged clusters
        @param smeasure: (SingleMeasure) class collecting measurement information during the process
        """
        pServ = ParticleService()
        temp_clusterList = clusterList.GET()
        temp_adatomList = adatomList.GET()
        
        x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
        y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
        r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])
        
        for adatom in temp_adatomList:
            x_square = (adatom.getX() - x_list)**2
            y_square = (adatom.getY() - y_list)**2
            distance_list = numpy.array(numpy.sqrt(x_square + y_square))
            
            
            clusters = (numpy.array(temp_clusterList))[distance_list <= (adatom.getR() + r_list)]
            if len(clusters)!=0:
                pServ.addAdatomtoCluster(initval, adatom, clusters[0], adatomList, clusterList, coalescenceList)
                smeasure.adatomEvent('clusterdeposition_sputter', 1)
            else:
                pServ.AdatomOnSurface(adatom, adatomList, adatomWWList, clusterList, coalescenceList)
                smeasure.adatomEvent('deposition_sputter', 1)
                
    def adatomWW(self, initval, adatomWWList, clusterList, coalescenceList, smeasure):
        """
        Finds overlapping radii and Event radii of adatoms with all the partcles on the
        surface, inclusively the adatoms themselves
        @param initval: (Initvals) class containing the system initial values
        @param adatomWWList: (ParticleList) Class with all adatoms deposited on the surface
        @param clusterList: (ParticleList) class contains all clusters
        @param coalescenceList: (PlList) class containing ParticleLists of merged clusters
        @param smeasure: (SingleMeasure) class collecting measurement information during the process
        """
        pServ = ParticleService()
        temp_clusterList = clusterList.GET()
        temp_adatomList = adatomWWList.GET()
        
        x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
        y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
        r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])
        rev_list = numpy.array([cluster.getREv() for cluster in temp_clusterList])
        
        
        for adatom in temp_adatomList:
            if adatom not in clusterList.GET():
                continue
            x_square = (adatom.getX() - x_list)**2
            y_square = (adatom.getY() - y_list)**2
            distance_list = numpy.array(numpy.sqrt(x_square + y_square))
            
            r_ol = (numpy.array(temp_clusterList))[(distance_list <= adatom.getR() + r_list)]
            rev_ol = (numpy.array(temp_clusterList))[(distance_list <= adatom.getREv() + rev_list)]
            
            ''' *** R Overlap *** '''
            r_ol_clear=[particle for particle in r_ol if 
                  (adatom!=particle and particle in clusterList.GET())]
            if len(r_ol_clear) != 0:
                if pServ.adatomClusterWW(initval, adatom, r_ol_clear[0], adatomWWList, clusterList, coalescenceList) == False:
                    continue
                
                if r_ol_clear[0].getN() == 1:
                    smeasure.adatomEvent('nucleation',1)
                else:
                    smeasure.adatomEvent('aggregation',1)
                continue

            ''' *** Rev Overlap for great WQS *** '''
            rev_ol_clear = [particle for particle in rev_ol if 
                            (particle not in r_ol and particle !=adatom and particle in clusterList.GET())]
            interaction = False
            if len(rev_ol_clear) != 0:
                for cluster in rev_ol_clear:
                    #print "AdatomWW check "+ str(self.checkGreatProhability(adatom, cluster))
                    if self.checkGreatProhability(adatom, cluster) >= 1:
                        if pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList) == False:
                            continue
                        
                        if cluster.getN() == 1:
                            smeasure.adatomEvent('nucleation',1)
                        else:
                            smeasure.adatomEvent('aggregation',1)
                        interaction = True
                        break
                
                ''' *** Rev Overlap for small WQS *** '''
                if interaction == False:
                    for cluster in rev_ol_clear:
                        WQS = self.getCollisionProhability(adatom, cluster)
                        #print "AdatomWW WQs "+ str(WQS)
                        if random() < WQS:
                            if pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList) == False:
                                continue
                            if cluster.getN() == 1:
                                smeasure.adatomEvent('nucleation',1)
                            else:
                                smeasure.adatomEvent('aggregation',1)
                            interaction = True
                            break
                        
    def coalescence(self, initval, clusterList, coalescenceList, smeasure):
        pServ = ParticleService()
        temp_clusterList = clusterList.GET()
        
        x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
        y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
        r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])
        rev_list = numpy.array([cluster.getREv() for cluster in temp_clusterList])
        
        for i, temp_pl in enumerate(coalescenceList.GET()):
            #check if particlelist is still in refreshed coalescenceList or its a null list
            if (temp_pl not in coalescenceList.GET()) or (temp_pl.clusterNumber()==0):
                continue
            for cluster in temp_pl:
                if (cluster not in clusterList.GET()):
                    continue
                x_square = (cluster.getX() - x_list)**2
                y_square = (cluster.getY() - y_list)**2
                distance_list = numpy.sqrt(x_square + y_square)
            
                r_ol = (numpy.array(temp_clusterList))[(distance_list <= cluster.getR() + r_list)]
                rev_ol = (numpy.array(temp_clusterList))[(distance_list <= cluster.getREv() + rev_list)]
            

                r_ol_clear = [particle for particle in r_ol if
                              (particle not in coalescenceList.getListbyIndex(i)) and (cluster != particle) and (particle in clusterList.GET())]
            

                #check for radius overlap
                if len(r_ol_clear) != 0:
                    for cluster2 in r_ol_clear:
                    
                        #in case of adatoms
                        if (cluster2.getN() == 1) and (coalescenceList.findCluster(cluster2).clusterNumber() == 1):
                            pServ.addParticleToCluster(initval, cluster2, cluster, clusterList, coalescenceList)
                            if cluster.getN() == 1:
                                smeasure.adatomEvent('nucleation', 1)
                            else:
                                smeasure.adatomEvent('aggregation', 1)
                        # for clusters or clustergroups        
                        else:
                            if pServ.addContact(cluster, cluster2):
                                pl_living = coalescenceList.getListbyIndex(i)
                                pl_destroyed = coalescenceList.findCluster(cluster2)
                                #transfer the particle objects and delete the empty particle list object
                                pServ.fuseParticleLists(pl_living, pl_destroyed, coalescenceList)
                            
            
            
                rev_ol_clear = [particle for particle in rev_ol if 
                                (particle not in coalescenceList.getListbyIndex(i)) and (particle not in r_ol_clear) and (particle != cluster)]
            
                if (len(rev_ol_clear)) != 0:
                    for cluster2 in rev_ol_clear:
                    
                        if self.calculateOverlap(cluster, cluster2, initval)>=1:
                            if (cluster2.getN() == 1) and (coalescenceList.findCluster(cluster2).clusterNumber() == 1):
                                pServ.addParticleToCluster(initval, cluster2, cluster, clusterList, coalescenceList)
                                if cluster.getN() == 1:
                                    smeasure.adatomEvent('nucleation', 1)
                                else:
                                    smeasure.adatomEvent('aggregation', 1)
                            # for clusters or clustergroups        
                            else:
                                if pServ.addContact(cluster, cluster2):
                                    pl_living = coalescenceList.getListbyIndex(i)
                                    pl_destroyed = coalescenceList.findCluster(cluster2)
                                    #transfer the particle objects and delete the empty particle list object
                                    pServ.fuseParticleLists(pl_living, pl_destroyed, coalescenceList)
                                
                                
    def calibrateCluster(self, pl):
        partServ = ParticleService()
        temp_pl = pl.GET()
        x_list = numpy.array([cluster.getX() for cluster in temp_pl])
        y_list = numpy.array([cluster.getY() for cluster in temp_pl])
        r_list = numpy.array([cluster.getR() for cluster in temp_pl])
        
        for cluster in temp_pl:
            x_square = (cluster.getX() - x_list)**2
            y_square = (cluster.getY() - y_list)**2
            distance_list = numpy.sqrt(x_square + y_square)
            
            r_ol = (numpy.array(temp_pl))[(distance_list <= cluster.getR() + r_list)]
            r_ol_clear = [elm for elm in r_ol if
                          (elm != cluster) and elm.getN()!=0 and elm not in cluster.getContacts()]
            
            # For clusters penetrating this cluster
            for interCluster in r_ol_clear:
                if interCluster.getN() > cluster.getN():
                    continue
                else:
                    partServ.clusterSurfaceTouching(cluster, interCluster)
            
            # To keep the slave cluster near the master cluster
            for adCluster in cluster.getContacts():
                if adCluster.getN() > cluster.getN():
                    continue
                else:
                    partServ.clusterSurfaceTouching(cluster, adCluster)     
            
            
    
            
    def convolutedGaussFunction(self, cluster, initval):
        # diffusion length / sqrt(12)
        R = cluster.getR()
        REv = cluster.getREv()
        sigma = (REv - R)/3.464
        
        #round value to prevent overflow 
        if (REv - R) < initval.getValue('radius'):
            #define a step function
            result = lambda r: 1.0*(r<=R or r>=-R)
            return result
        else:
            c = numpy.sqrt(2*numpy.pi)
            
            #define the gauss function in 1dim. with 2dim normalisation
            dist = lambda r: numpy.exp(-(r/sigma)**2/2.) / c / sigma
            
            #calculate the gauss with integration over the sphere
            result = lambda r: ( integrate.quad(dist, r-R, r+R, epsrel = 0.01) )[0]
            return result
        
        
    def calculateOverlap(self, cluster1, cluster2, initval):
        
        dist1 = self.convolutedGaussFunction(cluster1, initval)
        dist2 = self.convolutedGaussFunction(cluster2, initval)
        distance = numpy.sqrt((cluster1.getX()-cluster2.getX())**2 + (cluster1.getY()-cluster2.getY())**2)
        
        dist = lambda r: dist1(r)*dist2(r-distance)
        
        prohability = integrate.quad(dist, distance-cluster2.getREv(), cluster1.getREv(), epsrel = 0.01)
        return prohability
           
        
            
        