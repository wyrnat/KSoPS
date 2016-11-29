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
    Head Object of a single Simulation
    '''


    def __init__(self, myInitvals = None):
        '''
        Initializes needed Services
        creates global data objects
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
        
        print "sputter"
        print self.adatomList.GET()
  
        #WW of hits on surface or clusters
        self.adatomHits(self.initVal, self.adatomList, self.clusterList, self.coalescenceList ,smeasure) 
        
        
        
        #sort list starting with the biggest cluster group, move those groups
        self.coalescenceList.sortList()
        self.diffusion(self.initVal, self.clusterList, self.coalescenceList, smeasure)
        
        print "diffusion"
        print len(self.coalescenceList.GET()) 
        print len(self.clusterList.GET()) 
        
        #coalescence between all clusters
        self.coalescence(self.initVal, self.clusterList, self.coalescenceList, smeasure)
        print "before clearing"
        print len(self.coalescenceList.GET()) 
        print len(self.clusterList.GET())
        self.coalescenceList.clearList()
        
        print "coalescence"
        print len(self.coalescenceList.GET()) 
        print len(self.clusterList.GET())     
        
        #processes within cloalescencelist clusters
        self.atomFlow(self.initVal, self.clusterList, self.coalescenceList, smeasure)
        
        print "atomflow"
        print len(self.coalescenceList.GET()) 
        print len(self.clusterList.GET()) 
        
        # calibrate cluster distances
        self.calibrateDistance(self.initVal, self.clusterList, self.coalescenceList)
        
        
        #measures the actual state
        if ((self.simulation_step-1) % self.initVal.getValue("measure_steps") == 0):
            self.measurement(self.initVal, smeasure, self.measure, self.clusterList, self.coalescenceList, self.simulation_step)
        

        
        
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
            
    def adatomHits(self, initval, adatomList, clusterList, coalescenceList, smeasure):
        """
        Checks if particles from the adatomList collides with particles from the clusterList
        """
        intServ = InteractionService()
        intServ.adatomOnCluster(initval, adatomList, clusterList, coalescenceList, smeasure)
        
        
    def diffusion(self, initval, clusterList, coalescenceList, smeasure):
        """
        simulates brownian cluster motion with regard of boarders of the area
        """
        partServ = ParticleService()
        for pl in coalescenceList.GET():
            partServ.ClusterDiffusion(self.initVal, pl)
            
    def coalescence(self, initval, clusterList, coalescenceList, smeasure):
        """
        Searcing for overlapping clusters
        Fusing particleList
        """
        intServ = InteractionService()
        intServ.coalescence(initval, clusterList, coalescenceList, smeasure)       
        
        
    def atomFlow(self, initval, clusterList, coalescenceList, smeasure):
        """
        Checks if master value is correct
        let atoms aggregate from slave to master
        """
        partServ = ParticleService()
        clusterList.sortList(bigfirst=False)
        for cluster in clusterList.GET():
            partServ.atomFlow(initval, cluster, clusterList, coalescenceList, smeasure)
        coalescenceList.clearList()
        
        #refresh cluster parameter
        for cluster in clusterList.GET():
            partServ.refreshCluster(initval, cluster, coalescenceList)
        
    
    def calibrateDistance(self, initval, clusterList, coalescenceList):
        """
        Calibrates intern for every particleList in coalescenceList
        Search for overlap of particleList and when True, deplete a complete particleList
        """
        intServ = InteractionService()
        coalescenceList.sortList()
        
        #calibrate for each particleList in coalescenceList        
        intServ.calibrateIntern(initval, coalescenceList)
        #calibrate for all clusters
        intServ.calibrateCoalescence(initval, clusterList, coalescenceList)
            
            
    def measurement(self, initval, smeasure, measure, clusterList, coalescenceList, simulation_step):
        measServ = MeasureService()
        radius, distance, cluster_density, r_list, d_list, meancluster_plist = measServ.getMeanValues(initval, clusterList, coalescenceList)
        cluster_plist = measServ.getclusterPropList(clusterList)
        dist_ww = smeasure.GET()
        thickness = measServ.getThickness(initval, simulation_step)
        
        self.measure.save(thickness, radius, distance, cluster_density, r_list, d_list, dist_ww, meancluster_plist, cluster_plist)
        
    def showSimulation(self, step):
        self.screen.draw(self.initVal, self.measure.getClusterProperties(), step)
        