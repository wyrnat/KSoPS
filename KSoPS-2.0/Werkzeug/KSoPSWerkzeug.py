'''
Created on 15.10.2015

@author: jannik
'''

from Fachwerte.initVals import InitVals
from Fachwerte.singleMeasure import SingleMeasure
from Fachwerte.measure import Measure
from Materialien import particleList, plList

from Services.particleService import ParticleService
from Services.interactionService import InteractionService
from Services.initValService import InitValService
from Services.measureService import MeasureService

class Werkzeug(object):
    '''
    Regelt den Ablauf der Monte-Carlo Simulation
    '''


    def __init__(self):
        '''
        Initialisiert die Services und uebernimmt
        die GUI Parameter
        '''
        self.initVal = InitVals()
        self.adatomList = particleList.ParticleList()
        self.adatomWWList = particleList.ParticleList()
        self.clusterList = particleList.ParticleList()
        self.coalescenceList = plList.PlList()
        self.measure = Measure()
        
    def run(self, step):
        
        #instance of measurement for one period
        smeasure = SingleMeasure()
        
        #creates Adatoms and add them to adatomList
        self.sputter(self.adatomList)
        print "adatom "+str(len(self.adatomList.GET()))
        print "cluster "+str(len(self.clusterList.GET()))
        print "coalescence "+str(len(self.coalescenceList.GET()))
        print "***************"
        
        #WW midair and hits on surface or clusters
        self.adatomHits(self.initVal, self.adatomList, self.adatomWWList, self.clusterList, self.coalescenceList ,smeasure)
        print "adatom "+str(len(self.adatomList.GET()))
        print "cluster "+str(len(self.clusterList.GET()))
        print "coalescence "+str(len(self.coalescenceList.GET()))
        print "***************"
        
        #adatoms on Surface interacting with clusterList
        self.adatomWW(self.initVal, self.adatomWWList, self.clusterList, self.coalescenceList, smeasure)
        print "adatom "+str(len(self.adatomList.GET()))
        print "cluster "+str(len(self.clusterList.GET()))
        print "coalescence "+str(len(self.coalescenceList.GET()))
        print "***************"
        
        #move the rest, directly checking for collision
        self.diffusion(self.initVal, self.clusterList, self.coalescenceList)
        print "adatom "+str(len(self.adatomList.GET()))
        print "cluster "+str(len(self.clusterList.GET()))
        print "coalescence "+str(len(self.coalescenceList.GET()))
        print "***************"
        
        #processes within clusters or superclusters
        self.atomFlow(self.initVal, self.clusterList, self.coalescenceList)
        print "adatom "+str(len(self.adatomList.GET()))
        print "cluster "+str(len(self.clusterList.GET()))
        print "coalescence "+str(len(self.coalescenceList.GET()))
        print "***************"
        
        # calibrate cluster distances
        self.calibrateDistance(self.coalescenceList)
        
        #measures the actual state
        self.measurement(self.initVal, smeasure, self.measure, self.clusterList)
        
    """ *** Methods *** """
    
    def sputter(self, adatomList):
        #number of particles per ms to reach sputter rate
        initServ = InitValService()
        noa = initServ.getParticleRate(self.initVal)
        pServ = ParticleService()
        for i in range(noa):
            adatom = pServ.createAdatom(self.initVal)
            adatomList.addParticle(adatom)
            
    def adatomHits(self, initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure):
        intServ = InteractionService()
        intServ.adatomOnCluster(initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure)
        
    def adatomWW(self, initval, adatomWWList, clusterList, coalescenceList, smeasure):
        intServ = InteractionService()
        intServ.adatomWW(initval, adatomWWList, clusterList, coalescenceList, smeasure)
        
    def diffusion(self, initval, clusterList, coalescenceList):
        partServ = ParticleService()
        intServ = InteractionService()
        coalescenceList.sortList()
        for pl in coalescenceList.GET():
            if partServ.ClusterDiffusion(self.initVal, pl):
                intServ.diffusionOverlap(initval, pl, clusterList, coalescenceList)
        
        # delete all empty cluster lists        
        coalescenceList.clearList()
        
        
    def atomFlow(self, initval, clusterList, coalescenceList):
        partServ = ParticleService()
        for cluster in clusterList.GET():
            partServ.atomFlow(initval, cluster)
        partServ.deleteEmptyClusters(clusterList, coalescenceList)
        
        for cluster in clusterList.GET():
            partServ.refreshCluster(initval, cluster, coalescenceList)
        
    
    def calibrateDistance(self, coalescenceList):
        intServ = InteractionService()
        for Liste in coalescenceList.GET():
            intServ.calibrateCluster(Liste)
            
            
    def measurement(self, initval, smeasure, measure, clusterList):
        measServ = MeasureService()
        radius, distance, r_list, d_list, cluster_plist = measServ.getMeanValues(clusterList)
        dist_ww = smeasure.GET()
        thickness = measServ.getThickness(initval, clusterList)
        
        self.measure.save(thickness, radius, distance, r_list, d_list, dist_ww, cluster_plist)
        
            
        
        
                                     
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#     def adatomHits2(self):
#         """
#         Checks for adatoms to be deposited on surface or cluster
#         """
#         intServ = InteraktionService()
#         
#         #lists of hash values of clusters from particleList
#         hash_list, r_hits, rev_hits = intServ.getSputterOverlap(self.adatomList, self.particleList)
#         
#         #add adatoms overlapping with clusters to the cluster
#         for myhash_list in r_hits:
#             self.particleList.addToParticle(myhash_list[0], 1)
#         self.adatomList.removeParticles(r_hits)
#         
#         #check for adatoms with overlapping eventradius to a cluster
#         adatoms = self.adatomList.getParticles(hash_list)
#         for i, myhash in enumerate(rev_hits):
#             
#             particles = self.particleList.getHashList(myhash)
#             for particle in particles:
#             # fast calculation, if the prohability is cleary over 1
#                 distance = intServ.getParticleDistance(, y1, x2, y2)
#                 if intServ.checkGreatProhability(adatoms[i].getREv(), particle.getREv(),
#                                                  adatoms[i].getR(), particle.getR(),
#                                                   ) == True:
#                     self.particleList.addToParticle(myhash[0], 1)
#                     self.adatomList.removeParticles([hash_list[i]])
#                     break
#                 else:
#                     r_ad = self.adatomList.getParticles(myhash)
#                     prob = intServ.getCollisionProhability(self, radius_ev1, radius_ev2, radius1, radius2, distance)
#                 
#             
#             
#     
#     def move(self):
#         pass
#     
#     def Messung(self):
#         pass
#     
#     def InterclusterFluss(self):
#         pass
#     
#     def Kollisionen(self):
#         pass
#         