'''
Created on 15.10.2015

@author: woehnert
'''

from Fachwerte.initVals import InitVals
from Fachwerte.singleMeasure import SingleMeasure
from Fachwerte.measure import Measure
from Materialien import particleList, plList

from Services.particleService import ParticleService
from Services.interactionService import InteractionService
from Services.initValService import InitValService
from Services.measureService import MeasureService

from time import time

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
        
        #count number of simulation steps
        self.simulation_step = 0
        self.smeasure = SingleMeasure()      #instance of measurement for one measure period
        
    def run(self):
        
        ground = time()
        
        self.simulation_step += 1       #increase the step counter
        
        #creates Adatoms and add them to adatomList
        self.sputter(self.initVal, self.adatomList)
        
        Tsputter = time()
  
        #WW of hits on surface or clusters
        self.adatomHits(self.initVal, self.adatomList, self.clusterList, self.coalescenceList ,self.smeasure)
        
        Thits = time()
        
        #sort list starting with the biggest cluster group, move those groups
        self.coalescenceList.sortList()
        self.diffusion(self.initVal, self.clusterList, self.coalescenceList, self.smeasure)
        
        Tdiffusion = time()
        
        #coalescence between all clusters
        self.coalescence(self.initVal, self.clusterList, self.coalescenceList, self.smeasure)
        self.coalescenceList.clearList()
        
        Tcoalescence = time()
        
        #processes within cloalescencelist clusters
        self.atomFlow(self.initVal, self.clusterList, self.coalescenceList, self.smeasure)
        self.coalescenceList.clearList()
        
        Tflow = time()
        
        # calibrate cluster distances
        self.calibrateDistance(self.initVal, self.clusterList, self.coalescenceList)
        
        Tcalibrate = time()
        
        #measures the actual state
        if ((self.simulation_step-1) % self.initVal.getValue("measure_steps") == 0):
            self.measurement(self.initVal, self.smeasure, self.measure, self.clusterList, self.coalescenceList, self.simulation_step)
            #restart event measurement
            self.smeasure = SingleMeasure()
            
        Tmeasure = time()
        
        list = [(Tsputter - ground), (Thits - Tsputter),
                (Tdiffusion - Thits), (Tcoalescence - Tdiffusion),
                (Tflow - Tcoalescence), (Tcalibrate - Tflow),
                (Tmeasure - Tflow), (Tmeasure-ground)]
        
        return list
        

        
        
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
        intServ.calibrateIntern(initval, clusterList, coalescenceList)
        #calibrate for all clusters
        intServ.calibrateCoalescence(initval, clusterList, coalescenceList)
            
            
    def measurement(self, initval, smeasure, measure, clusterList, coalescenceList, simulation_step):
        measServ = MeasureService()
        radius, distance, cluster_density, r_list, d_list = measServ.getMeanValues(initval, clusterList, coalescenceList)
        cluster_plist = measServ.getclusterPropList(clusterList)
        dist_ww = smeasure.GET()
        #norm dist_ww on measure_steps
        for i in dist_ww:
            dist_ww[i] = dist_ww[i]/(1.0*initval.getValue('measure_steps'))
        time, thickness = measServ.getTimeThickness(initval, simulation_step)
        
        self.measure.save(time, thickness, radius, distance, cluster_density, r_list, d_list, dist_ww, cluster_plist)
        