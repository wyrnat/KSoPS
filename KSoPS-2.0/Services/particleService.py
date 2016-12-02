'''
Created on 15.10.2015

@author: Jannik Woehnert
'''

import random
import numpy
from scipy import integrate
from Fachwerte.particle import Particle
from Services.initValService import InitValService


class ParticleService(object):
    '''
    classdocs
    '''
    sqrt3 = numpy.sqrt(3)

    def __init__(self):
        '''
        Constructor
        '''
        
    """ Sputter """ 
           
    def createAdatom(self, initval):
        """
        Erzeugt ein Adatom und
        fuegt es zur Liste hinzu
        """
        assert(initval.getValue('area') > 0), 'erzeugeAdatome: Area zu klein'
        assert(initval.getValue('radius') > 0), 'erzeugeAdatome: Radius zu klein'
        
        initServ = InitValService()
        
        x = (random.random() - 0.5) * initval.getValue('area')
        y = (random.random() - 0.5) * initval.getValue('area')
        r = initval.getValue('radius')
        rev = initServ.getAdatomEventRadius(initval) + r
        
        adatom = Particle(x,y,r,rev)
        
        return adatom
    





    
    """ Adatom Hits """
        
    def AdatomOnSurface(self, adatom, adatomList, clusterList, coalescenceList):
        p = adatomList.removeParticle(adatom)
        clusterList.addParticle(adatom)
        #adatomWWList.addParticle(p)
        coalescenceList.addAdatom(adatom)
            
            
    def addAdatomtoCluster(self, initval, adatom, cluster, adatomList, clusterList, coalescenceList): 
        adatomList.removeParticle(adatom)
        cluster.atomFlow(1)
        self.refreshCluster(initval, cluster, coalescenceList)
            
    def addParticleToCluster(self, initval, particle, cluster, clusterList, coalescenceList):
        assert (particle in clusterList.GET()), "addparticleToCluster: particle not in particlelist"
        assert (cluster in clusterList.GET()), "addparticleToCluster: cluster not in particlelist"
        clusterList.removeParticle(particle)
        coalescenceList.removeCluster(particle)
        cluster.atomFlow(particle.getN())
        self.refreshCluster(initval, cluster, coalescenceList)








            

    
    
    
    """ Diffusion """
            
    def ClusterDiffusion(self, initval, pl):
        assert(pl.clusterNumber() != 0), 'ClusterDiffusion: No clusters in this list'
        
        rndm = random.random()
        move = pl.GET()[0].getREv() - pl.GET()[0].getR()
        
        #if movement is significant
        if move > initval.getValue('radius')*0.01:
            G = numpy.random.normal(0,move/3.464)
            dx = G * numpy.sin(2 * numpy.pi * rndm)
            dy = G * numpy.cos(2 * numpy.pi * rndm)
            pl.moveAll(dx, dy)
        
        
        ndx, ndy = self.checkBorders(initval, pl)
        pl.moveAll(ndx,ndy)
        
    def checkBorders(self, initval, plist):
        """
        Check for cluster movement, if it will defy the area borders.
        shortens dx, dy if necessary
        """
        boarder = initval.getValue('area')/2.
        pl = plist.GET()
        
        #the wanted translation
        ndx = 0
        ndy = 0
        left = [(cluster.getX()-cluster.getR()) for cluster in pl]#.sort()
        right = [(cluster.getX()+cluster.getR()) for cluster in pl]#.sort(reverse=True)
        top = [(cluster.getY()-cluster.getR()) for cluster in pl]#.sort()
        bottom = [(cluster.getY()+cluster.getR()) for cluster in pl]#.sort(reverse=True)
        left.sort()
        right.sort(reverse=True)
        top.sort()
        bottom.sort(reverse=True)
        
        if left[0]<-boarder:
            ndx = -boarder-left[0]
        if right[0]>boarder:
            ndx = boarder-right[0]
        if top[0]<-boarder:
            ndy = -boarder-top[0]
        if bottom[0]>boarder:
            ndy = boarder-bottom[0]
            
        return ndx, ndy
        
        
        
        



    
    """ Coalescence """
    
    def addContact(self, cluster1, cluster2):
        
        if cluster1.getN()>=cluster2.getN():
            if cluster2.getMaster() == None:
                cluster2.setMaster(cluster1)
                return True
        return False
    
    def fuseParticleLists(self, pl1, pl2, coalescenceList):
        assert (pl1 in coalescenceList.GET()), "fuseparticleLists: pl1 not in coalescenceList"
        assert (pl2 in coalescenceList.GET()), "fuseparticleLists: pl2 not in coalescenceList"
        for particle in pl2.GET():
            pl2.removeParticle(particle)
            pl1.addParticle(particle)
        coalescenceList.removePl(pl2)
        
    def convolutedGaussFunction(self, cluster, initval):
        # diffusion length / sqrt(12)
        R = cluster.getR()
        REv = cluster.getREv()
        sigma = (REv - R)/3.464
        
        #round value to prevent overflow 
        if (REv - R) < initval.getValue('radius')*0.01:
            #define a step function
            result = lambda r: 1.0*(r<=R and r>=-R)
            return result
        else:
            c = numpy.sqrt(2*numpy.pi)
            
            #define the gauss function in 1dim. with 2dim normalisation
            dist = lambda r: numpy.exp(-(r/sigma)**2/2.) / c / sigma
            
            #calculate the gauss with integration over the sphere
            result = lambda r: (integrate.quad(dist, r-R, r+R, epsrel = 0.01))[0] * ( (REv-R)/initval.getValue('lattice_const'))**2
            return result
        
    def calculateOverlap(self, cluster1, cluster2, initval):
        
        dist1 = self.convolutedGaussFunction(cluster1, initval)
        dist2 = self.convolutedGaussFunction(cluster2, initval)
        REv1 = cluster1.getREv()
        REv2 = cluster2.getREv()
        distance = numpy.sqrt((cluster1.getX()-cluster2.getX())**2 + (cluster1.getY()-cluster2.getY())**2)
        #ThreeD_Factor = numpy.arctan(REv1/distance) * numpy.arctan(REv2/distance) / numpy.pi**2
        
        dist = lambda r: dist1(r)*dist2(r-distance) #* ThreeD_Factor
        
        prohability = integrate.quad(dist, distance-REv2, REv1, epsrel = 0.01)
        return prohability
        
        
    
    
    
    
        
        
        
    """ atomFLow """
            
    def atomFlow(self, initval, cluster, clusterList, coalescenceList, smeasure):
        initServ = InitValService()
        if cluster.getMaster() == None:
            return
        if cluster.getMaster() not in clusterList.GET():
            cluster.deleteMaster()
            return
        if cluster.getN() > cluster.getMaster().getN():
            if (cluster.getMaster().getMaster() == None):
                oldmaster = cluster.getMaster()
                cluster.deleteMaster()
                oldmaster.setMaster(cluster)
                return
            cluster.deleteMaster()
            return
        
        distance = numpy.sqrt((cluster.getX()-cluster.getMaster().getX())**2 + (cluster.getY()-cluster.getMaster().getY())**2)
        R = cluster.getMaster().getR()
        n = cluster.getSurfaceN()
        ThreeD_Factor = (n > 12)*(numpy.arctan(R/distance) / numpy.pi) + 1*(n <=12)
        flow = initServ.getAtomFlow(initval, int(numpy.ceil(cluster.getSurfaceN()*ThreeD_Factor)))
        
        
        if flow == 0:
            return
        
        if flow >= cluster.getN():
            cluster.getMaster().atomFlow(cluster.getN())
            clusterList.removeParticle(cluster)
            coalescenceList.removeCluster(cluster)
            smeasure.adatomEvent('coalescence', cluster.getN())
        else:
            cluster.getMaster().atomFlow(flow)
            cluster.atomFlow(-flow)
            smeasure.adatomEvent('coalescence', flow)
            
    def refreshCluster(self, initval, cluster, coalescenceList):
        self.setClusterR(initval, cluster)
        self.setSurfaceAtoms(initval, cluster)
        liste = coalescenceList.findCluster(cluster)
        allN = liste.getAllN()
        self.setClusterRev(initval, cluster, allN)
        
    def setClusterR(self, initval, cluster):
        initServ = InitValService()
        if cluster.getN() < 2:
            R = initval.getValue('radius')
        else:
            R = initServ.getR(initval, cluster.getN())
        cluster.setR(R) 
        
    def setSurfaceAtoms(self, initval, cluster):
        initServ = InitValService()
        R = cluster.getR()
        N = cluster.getN()
        if N>12:
            cluster.setSurfaceN( initServ.getSurfaceN(initval, R) )
        else:
            cluster.setSurfaceN(N)   

    def setClusterRev(self, initval, cluster, allN):
        """
        Gets the interface Atoms of the clusters
        associated with a coalescence group and
        calculates the event radius
        """
        assert (type(allN) == int ), 'setClusterRev: allN type not Integer'
        
        initServ = InitValService()
        R = cluster.getR()
        rev = initServ.getREv(initval, allN)
        if rev > initval.getValue('radius')*0.1:
            cluster.setREv( rev + R )
        else:
            cluster.setREv(R)     
        
        
        

    



                    
    """ calibrateDistance """
        
    def clusterSurfaceTouching(self, master, slave):
        """
        Move slave to get in touch with the surface of master
        """
        assert(master != slave), "particleService.clusterSurfaceTouching: particles identical"
        assert(master.getN()>=slave.getN()), "particleService.clusterSurfaceTouching: master smaller than slave"
        dir_x =  master.getX() - slave.getX()
        dir_y =  master.getY() - slave.getY()
        distance = numpy.sqrt( (dir_x)**2 + (dir_y)**2 )
        radius = master.getR() + slave.getR()
        
        x = slave.getX() + dir_x * (distance - radius) / distance
        y = slave.getY() + dir_y * (distance - radius) / distance
        
        #return new position of slave
        return x, y
        








    """ Measurement """

    def getParticleDistance(self, cluster1, cluster2):
        dir_x = cluster1.getX() - cluster2.getX()
        dir_y = cluster1.getY() - cluster2.getY()
        return numpy.sqrt( (dir_x)**2 + (dir_y)**2 ) 
    

       
    

                 
    
        
#     def addContact(self, cluster1, cluster2):
#         """
#         add the clusters to each others contact lists
#         """
#         #print "particleService.addContact() pre "+str(cluster1.getN()) + "  "+ str(cluster2.getN())
#         if cluster2 in cluster1.getContacts():
#             return False
#         if cluster1.getN() < cluster2.getN():
#             for adCluster in cluster1.getContacts():
#                 if adCluster.getN() > cluster1.getN():
#                     return False
#             cluster1.addContacts([cluster2])
#             cluster2.addContacts([cluster1])
#             return True
#             
#         elif cluster1.getN() > cluster2.getN():
#             for adCluster in cluster2.getContacts():
#                 if adCluster.getN() > cluster2.getN():
#                     return False
#             cluster1.addContacts([cluster2])
#             cluster2.addContacts([cluster1])
#             return True
#         
#         else:
#             isthebiggest = True
#             for adCluster in cluster1.getContacts():
#                 if adCluster.getN() > cluster1.getN():
#                     isthebiggest = False
#                     break
#             for adCluster in cluster2.getContacts():
#                 if adCluster.getN() > cluster2.getN() and isthebiggest == False:
#                     return False
#             #print "particleService.addContact() post "+str(cluster1.getN()) + "  "+ str(cluster2.getN())   
#             cluster1.addContacts([cluster2])
#             cluster2.addContacts([cluster1])
#             return True
            
        
#     def setInterfaceAtoms(self, initval, cluster):
#         r = initval.getValue('radius')
#         R = cluster.getR()
#         cluster.setInterN(numpy.ceil( numpy.sqrt(2) * numpy.pi / 8. * R**2 / r**2 ))

#     def deleteEmptyClusters(self, clusterList, coalescenceList):
#         for cluster in clusterList.GET():
#             if cluster.getN() == 0:
#                 clusterList.removeParticle(cluster)
#                 coalescenceList.removeCluster(cluster)
#                 for contact in cluster.getContacts():




#         for cluster in pl.GET():
#             R = cluster.getR()
#             x = cluster.getX()
#             y = cluster.getY()
#             if (abs(x + ndx) + R > area /2.):
#                 if (x+ndx) > 0:
#                     ndx = area/2. - x - R
#                 else:
#                     ndx = -area/2. - x + R
#                 
#             if abs(y + ndy) + R > area /2.:
#                 if (y+ndy) > 0:
#                     ndy = area/2. - y - R
#                 else:
#                     ndy = -area/2. - y + R
#                 
#         return ndx , ndy
#                     contact.removeContacts([cluster])
#         coalescenceList.clearList()



#     def getFusedREv(self, initval, pl):
#         initServ = InitValService()
#         N = pl.getInterN()
#         return initServ.getREv(initval, N)


#     """ Adatom WW """        
#             
#     def adatomClusterWW(self, initval, adatom, cluster, adatomWWList, clusterList, coalescenceList):
#         """
#         Handles the adatoms who were deposited on the substrate
#         They are within adatomWWList and ClusterList
#         """
#         if (cluster in clusterList.GET()) and (clusterList.removeParticle(adatom) != None):
#             adatomWWList.removeParticle(adatom)
#             cluster.atomFlow(1)
#             coalescenceList.removeCluster(adatom)
#             self.refreshCluster(initval, cluster, coalescenceList)
#             return True
#         return False
        
        