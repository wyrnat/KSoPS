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
from UI.pygameUI import PygameUI

class Werkzeug(object):
    '''
    Regelt den Ablauf der Monte-Carlo Simulation
    '''


    def __init__(self, myInitvals = None):
        '''
        Initialisiert die Services und uebernimmt
        die GUI Parameter
        '''
        
        self.initVal = InitVals(myInitvals)
        self.adatomList = particleList.ParticleList()
        #self.adatomWWList = particleList.ParticleList()
        self.clusterList = particleList.ParticleList()
        self.coalescenceList = plList.PlList()
        self.measure = Measure()
        self.screen = PygameUI(self.initVal)
        
        #count number of simulation steps
        self.simulation_step = 0
        
    def run(self):
        
        smeasure = SingleMeasure()      #instance of measurement for one period
        self.simulation_step += 1       #increase the step counter
        
        #creates Adatoms and add them to adatomList
        self.sputter(self.initVal, self.adatomList)
  
        #WW of hits on surface or clusters
        self.adatomHits(self.initVal, self.adatomList, self.adatomWWList, self.clusterList, self.coalescenceList ,smeasure)        
        
        #sort list starting with the biggest cluster group, move those groups
        self.coalescenceList.sortList()
        self.diffusion(self.initVal, self.clusterList, self.coalescenceList, smeasure)
        
        #coalescence between all clusters
        self.coalescence(self.initVal, self.clusterList, self.coalescenceList, smeasure)
        self.coalescenceList.clearList()        
        
        #processes within cloalescencelist clusters
        self.atomFlow(self.initVal, self.clusterList, self.coalescenceList)
        
        # calibrate cluster distances
        self.calibrateDistance(self.coalescenceList)
        
        
        #measures the actual state
        if ((self.simulation_step-1) % self.initVal.getValue("measure_steps") == 0):
            self.measurement(self.initVal, smeasure, self.measure, self.clusterList, self.simulation_step)
        
        # shows the simulation
        self.showSimulation(self.initVal, self.measure, self.simulation_step)
        
        
    """ *** Methods *** """
    
    def sputter(self, initval, adatomList):
        """
        Creates fresh adatoms and puts them into the adatomList
        """
        #number of particles per ms to reach sputter rate
        initServ = InitValService()
        noa = initServ.getParticleRate(initval)
        pServ = ParticleService()
        for i in range(noa):
            adatom = pServ.createAdatom(initval)
            adatomList.addParticle(adatom)
            
    def adatomHits(self, initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure):
        """
        Checks if particles from the adatomList collides with particles from the clusterList
        """
        intServ = InteractionService()
        intServ.adatomOnCluster(initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure)
        
#     def adatomWW(self, initval, adatomWWList, clusterList, coalescenceList, smeasure):
#         intServ = InteractionService()
#         intServ.adatomWW(initval, adatomWWList, clusterList, coalescenceList, smeasure)
        
    def diffusion(self, initval, clusterList, coalescenceList, smeasure):
        partServ = ParticleService()
        for pl in coalescenceList.GET():
            partServ.ClusterDiffusion(self.initVal, pl)
            
    def coalescence(self, initval, clusterList, coalescenceList, smeasure):
        intServ = InteractionService()
        intServ.coalescence(initval, clusterList, coalescenceList, smeasure)       
        
        
    def atomFlow(self, initval, clusterList, coalescenceList):
        partServ = ParticleService()
        for cluster in clusterList.GET():
            partServ.atomFlow(initval, cluster, clusterList)
        partServ.deleteEmptyClusters(clusterList, coalescenceList)
        
        for cluster in clusterList.GET():
            partServ.refreshCluster(initval, cluster, coalescenceList)
        
    
    def calibrateDistance(self, coalescenceList):
        intServ = InteractionService()
        for pl in coalescenceList.GET():
            intServ.calibrateCluster(pl)
            
            
    def measurement(self, initval, smeasure, measure, clusterList, simulation_step):
        measServ = MeasureService()
        radius, distance, r_list, d_list, cluster_plist = measServ.getMeanValues(clusterList)
        dist_ww = smeasure.GET()
        thickness = measServ.getThickness(initval, simulation_step)
        cluster_density = len(clusterList)/float(initval.getValue('area')**2)
        
        self.measure.save(thickness, radius, distance, cluster_density, r_list, d_list, dist_ww, cluster_plist)
        
    def showSimulation(self, initval, measure, step):
        self.screen.draw(initval, measure, step)
        
        
        #         print "***** Sputter"
#         coalescenceNumber = []
#         coalescenceNumber = []
#         positionNumber = []
#         for mylist in self.coalescenceList.GET():
#             coalescenceNumber.append(mylist.GET())
#         for particle in self.clusterList.GET():
#             positionNumber.append(str(round(particle.x,3))+";"+str(round(particle.y,3)))
#         print "CoalescenceList: ",coalescenceNumber
#         print "ClusterList: ",self.clusterList.GET()
#         print "clusterPos: ", positionNumber
#         print "AdatomWWList: ",len(self.adatomWWList.GET())
        