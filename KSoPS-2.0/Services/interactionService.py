'''
Created on 19.10.2015

@author: jannik
'''
import numpy
from particleService import ParticleService
from random import random

class InteractionService(object):
    '''
    classdocs
    '''

        
    def adatomOnCluster(self, initval, adatomList, clusterList, coalescenceList, smeasure):
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
                pServ.AdatomOnSurface(adatom, adatomList, clusterList, coalescenceList)
                smeasure.adatomEvent('deposition_sputter', 1)
                
    
                        
    def coalescence(self, initval, clusterList, coalescenceList, smeasure):
        pServ = ParticleService()
        temp_clusterList = clusterList.GET()
        temp_coalescenceList = coalescenceList.GET()
        
        x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
        y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
        r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])
        rev_list = numpy.array([cluster.getREv() for cluster in temp_clusterList])
        
        for i, temp_pl in enumerate(coalescenceList.GET()):
            #check if particlelist is still in refreshed coalescenceList or its a null list
            if (temp_pl not in coalescenceList.GET()) or (temp_pl.clusterNumber()==0):
                continue
            for cluster in temp_pl.GET():
                if (cluster not in clusterList.GET()):
                    continue
                x_square = (cluster.getX() - x_list)**2
                y_square = (cluster.getY() - y_list)**2
                distance_list = numpy.sqrt(x_square + y_square)
            
                r_ol = (numpy.array(temp_clusterList))[(distance_list < cluster.getR() + r_list)]
                rev_ol = (numpy.array(temp_clusterList))[(distance_list < cluster.getREv() + rev_list)]
            
                #not a hit if 
                r_ol_clear = [particle for particle in r_ol if
                              (particle in clusterList.GET())
                              and (particle.getMaster() == None)
                              and (particle not in coalescenceList.getListbyIndex(i).GET())
                              and (cluster != particle)
                              and (i < coalescenceList.getIndexByCluster(particle))
                              and ( temp_coalescenceList[coalescenceList.getIndexByCluster(particle)].hasCluster(particle) )
                              ]
             
 
                #check for radius overlap
                if len(r_ol_clear) != 0:
                    for cluster2 in r_ol_clear:
                     
                        #in case of adatoms
                        if (cluster2.getN() == 1) and (coalescenceList.findCluster(cluster2).clusterNumber() == 1):
                            pServ.addParticleToCluster(initval, cluster2, cluster, clusterList, coalescenceList)
                            if cluster.getN() == 2:
                                smeasure.adatomEvent('nucleation', 1)
                            else:
                                smeasure.adatomEvent('aggregation', 1)
                                
                        # for clusters or clustergroups        
                        else:
                            if pServ.addContact(cluster, cluster2):
                                pl_living = coalescenceList.findCluster(cluster)
                                pl_destroyed = coalescenceList.findCluster(cluster2)
                                #transfer the particle objects and delete the empty particle list object
                                pServ.fuseParticleLists(pl_living, pl_destroyed, coalescenceList)
                            
            
            
                rev_ol_clear = [particle for particle in rev_ol if 
                                (particle in clusterList.GET())
                                and (particle.getMaster() == None)
                                and (particle not in coalescenceList.getListbyIndex(i).GET())
                                and (particle != cluster)
                                and (particle not in r_ol_clear)
                                and (i < coalescenceList.getIndexByCluster(particle))
                                and ( temp_coalescenceList[coalescenceList.getIndexByCluster(particle)].hasCluster(particle) ) 
                                ] 
            
                if (len(rev_ol_clear)) != 0:
                    for cluster2 in rev_ol_clear:
                        
                        rndm = random()
                        probably = (rndm < 0.01)
                        if probably == False:
                            prohability = pServ.calculateOverlap(cluster, cluster2, initval)[0]
                        else:
                            prohability = 1
                        if prohability>rndm:
                            if (cluster2.getN() == 1) and (coalescenceList.findCluster(cluster2).clusterNumber() == 1):
                                pServ.addParticleToCluster(initval, cluster2, cluster, clusterList, coalescenceList)
                                if cluster.getN() == 2:
                                    smeasure.adatomEvent('nucleation', 1)
                                else:
                                    smeasure.adatomEvent('aggregation', 1)

                            # for clusters or clustergroups        
                            else:
                                if pServ.addContact(cluster, cluster2):
                                    pl_living = coalescenceList.findCluster(cluster)
                                    pl_destroyed = coalescenceList.findCluster(cluster2)
                                    #transfer the particle objects and delete the empty particle list object
                                    pServ.fuseParticleLists(pl_living, pl_destroyed, coalescenceList)
                                   
                                
                                
    def calibrateCoalescence(self, initval, clusterlist, coalescencelist):
        #TODO: slaves to master bewegen, danach ueberlappungen beseitigen        

        partServ = ParticleService()
        temp_clusterList = clusterlist.GET()
        x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
        y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
        r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])              
        for i, pl in enumerate(coalescencelist.GET()): 
            for cluster in pl.GET():
                x_square = (cluster.getX() - x_list)**2
                y_square = (cluster.getY() - y_list)**2
                distance_list = numpy.sqrt(x_square + y_square)
            
                r_ol = (numpy.array(temp_clusterList))[(distance_list <= cluster.getR() + r_list)]
                
                #overlapping cluster is not in coalescenceList and also in a coalescenceList smaller equal the recent one
                r_ol_clear = [elm for elm in r_ol if
                              (elm != cluster) and (elm not in pl.GET())
                              and (coalescencelist.getIndex(coalescencelist.findCluster(elm))>i)]
            
            
            
                # move smaller particleList away
                for interCluster in r_ol_clear:
                    if cluster.getR()+interCluster.getR() > partServ.getParticleDistance(cluster, interCluster):
                        continue
                    else:
                        x, y = partServ.clusterSurfaceTouching(cluster, interCluster)
                        coalescencelist.findCluster(interCluster).moveAll(x-interCluster.getX(), y-interCluster.getY())
                
    
    def calibrateIntern(self, initval, clusterList, coalescencelist):
        partServ = ParticleService()
        for pl in coalescencelist.GET():
            if pl.clusterNumber() == 1:
                continue
            pl.sortList()
            for j, cluster in enumerate(pl.GET()):
                if (cluster.getMaster() not in clusterList.GET()) and (cluster.getMaster() != None):
                    cluster.deleteMaster()
                assert(cluster != cluster.getMaster()), 'calibrateIntern: calibrateCLuster: cluster is his own master'
                assert((cluster.getMaster() in pl.GET()) or cluster.getMaster() == None), 'calibrateIntern: master of cluster not in same particleList'
                if (cluster.getMaster() == None):
                    if j!=0:
                        distance = 10.0*initval.getValue('area')
                        chef_cluster = None
                        for chef in pl.GET()[:j]:
                            newdistance = partServ.getParticleDistance(chef, cluster)
                            if (distance > newdistance) and (cluster.getN()<=chef.getN()) and (chef != cluster):
                                distance = newdistance
                                chef_cluster = chef
                        if chef_cluster != None:        
                            cluster.setMaster(chef_cluster)
                        else:
                            continue
                    else:
                        continue
                if cluster.getMaster().getN() < cluster.getN():
                    continue
                x, y = partServ.clusterSurfaceTouching(master=cluster.getMaster(), slave=cluster)
                cluster.setX(x)
                cluster.setY(y)
    
            
    
           
        
            
# def adatomWW(self, initval, adatomWWList, clusterList, coalescenceList, smeasure):
#         """
#         Finds overlapping radii and Event radii of adatoms with all the partcles on the
#         surface, inclusively the adatoms themselves
#         @param initval: (Initvals) class containing the system initial values
#         @param adatomWWList: (ParticleList) Class with all adatoms deposited on the surface
#         @param clusterList: (ParticleList) class contains all clusters
#         @param coalescenceList: (PlList) class containing ParticleLists of merged clusters
#         @param smeasure: (SingleMeasure) class collecting measurement information during the process
#         """
#         pServ = ParticleService()
#         temp_clusterList = clusterList.GET()
#         temp_adatomList = adatomWWList.GET()
#         
#         x_list = numpy.array([cluster.getX() for cluster in temp_clusterList])
#         y_list = numpy.array([cluster.getY() for cluster in temp_clusterList])
#         r_list = numpy.array([cluster.getR() for cluster in temp_clusterList])
#         rev_list = numpy.array([cluster.getREv() for cluster in temp_clusterList])
#         
#         
#         for adatom in temp_adatomList:
#             if adatom not in clusterList.GET():
#                 continue
#             x_square = (adatom.getX() - x_list)**2
#             y_square = (adatom.getY() - y_list)**2
#             distance_list = numpy.array(numpy.sqrt(x_square + y_square))
#             
#             r_ol = (numpy.array(temp_clusterList))[(distance_list <= adatom.getR() + r_list)]
#             rev_ol = (numpy.array(temp_clusterList))[(distance_list <= adatom.getREv() + rev_list)]
#             
#             ''' *** R Overlap *** '''
#             r_ol_clear=[particle for particle in r_ol if 
#                   (adatom!=particle and particle in clusterList.GET())]
#             if len(r_ol_clear) != 0:
#                 if pServ.adatomClusterWW(initval, adatom, r_ol_clear[0], adatomWWList, clusterList, coalescenceList) == False:
#                     continue
#                 
#                 if r_ol_clear[0].getN() == 1:
#                     smeasure.adatomEvent('nucleation',1)
#                 else:
#                     smeasure.adatomEvent('aggregation',1)
#                 continue
# 
#             ''' *** Rev Overlap for great WQS *** '''
#             rev_ol_clear = [particle for particle in rev_ol if 
#                             (particle not in r_ol and particle !=adatom and particle in clusterList.GET())]
#             interaction = False
#             if len(rev_ol_clear) != 0:
#                 for cluster in rev_ol_clear:
#                     #print "AdatomWW check "+ str(self.checkGreatProhability(adatom, cluster))
#                     if self.checkGreatProhability(adatom, cluster) >= 1:
#                         if pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList) == False:
#                             continue
#                         
#                         if cluster.getN() == 1:
#                             smeasure.adatomEvent('nucleation',1)
#                         else:
#                             smeasure.adatomEvent('aggregation',1)
#                         interaction = True
#                         break
#                 
#                 ''' *** Rev Overlap for small WQS *** '''
#                 if interaction == False:
#                     for cluster in rev_ol_clear:
#                         WQS = self.getCollisionProhability(adatom, cluster)
#                         #print "AdatomWW WQs "+ str(WQS)
#                         if random() < WQS:
#                             if pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList) == False:
#                                 continue
#                             if cluster.getN() == 1:
#                                 smeasure.adatomEvent('nucleation',1)
#                             else:
#                                 smeasure.adatomEvent('aggregation',1)
#                             interaction = True
#                             break