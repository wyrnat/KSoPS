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
        if pl.clusterNumber() == 0:
            return False
        
        rndm = random.random()
        move = pl.GET()[0].getREv() - pl.GET()[0].getR()
        #create Gaussian      
        
        #if movement is significant
        if move > initval.getValue('radius'):
            G = numpy.random.normal(0,move/3.464)
            dx = G * numpy.sin(2 * numpy.pi * rndm)
            dy = G * numpy.cos(2 * numpy.pi * rndm)
            dx, dy = self.checkBorders(initval, pl, dx, dy)
            pl.moveAll(dx, dy)
            return True
        #otherwise check only for particle on area
        else:
            dx, dy = self.checkBorders(initval, pl, 0,0)
            pl.moveAll(dx,dy)
            return False
        
    def checkBorders(self, initval, pl, dx, dy):
        """
        Check for cluster movement, if it will defy the area borders.
        shortens dx, dy if necessary
        """
        area = initval.getValue('area')
        
        #the wanted translation
        ndx = dx
        ndy = dy
        
        for cluster in pl.GET():
            R = cluster.getR()
            x = cluster.getX()
            y = cluster.getY()
            if (abs(x + ndx) + R > area /2.):
                if (x+ndx) > 0:
                    ndx = area/2. - x - R
                else:
                    ndx = -area/2. - x + R
                
            if abs(y + ndy) + R > area /2.:
                if (y+ndy) > 0:
                    ndy = area/2. - y - R
                else:
                    ndy = -area/2. - y + R
                
        return ndx , ndy







    
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
        if (REv - R) < initval.getValue('radius'):
            #define a step function
            result = lambda r: 1.0*(r<=R or r>=-R)
            return result
        else:
            c = numpy.sqrt(2*numpy.pi)
            
            #define the gauss function in 1dim. with 2dim normalisation
            dist = lambda r: numpy.exp(-(r/sigma)**2/2.) / c / sigma
            
            #calculate the gauss with integration over the sphere
            result = lambda r: ( integrate.quad(dist, r-R, r+R, epsrel = 0.01) )[0] * ( (REv-R)/initval.getValue('lattice_const'))**2
            #print "prob_max: "+ str(result(0))
            return result
        
    def calculateOverlap(self, cluster1, cluster2, initval):
        
        dist1 = self.convolutedGaussFunction(cluster1, initval)
        dist2 = self.convolutedGaussFunction(cluster2, initval)
        distance = numpy.sqrt((cluster1.getX()-cluster2.getX())**2 + (cluster1.getY()-cluster2.getY())**2)
        
        dist = lambda r: dist1(r)*dist2(r-distance)
        
        prohability = integrate.quad(dist, -cluster2.getREv(), distance+cluster1.getREv(), epsrel = 0.01)
#         print "***calculateOverlap***"
#         print "r: "+str(cluster1.getREv())+", "+str(cluster2.getREv())
#         print "distance: "+str(distance)
#         print"prohability: "+str(prohability[0])
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
        
        flow = initServ.getAtomFlow(initval, cluster.getR())
        
        print "AtomFLow"
        print "N: "+str(cluster.getN())
        print "flow: "+str(flow)
        
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
        if cluster.getN() < 2:
            R = initval.getValue('radius')
        else:
            R = numpy.power(6*numpy.sqrt(2)/numpy.pi * cluster.getN(), 1/3.) * initval.getValue('radius')
        cluster.setR(R) 
        
    def setSurfaceAtoms(self, initval, cluster):
        r = initval.getValue('radius')
        R = cluster.getR()
        N = cluster.getN()
        if N>12:
            cluster.setSurfaceN( numpy.floor(numpy.pi/3./numpy.sqrt(2)*(6*R**2/r**2 - 12*R/r + 8)) )
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
        if rev > initval.getValue('radius'):
            cluster.setREv( rev + R )
        else:
            cluster.setREv(R)     
        
        
        

    



                    
    """ calibrateDistance """
        
    def clusterSurfaceTouching(self, cluster1, cluster2):
        """
        Move cluster2 to get in touch with the surface of cluster1
        """
        assert(cluster1 != cluster2), "particleService.clusterSurfaceTouching: particles identical"
        assert(cluster1.getN()>=cluster2.getN()), "particleService.clusterSurfaceTouching: cluster1 smaller than cluster2"
        dir_x = cluster1.getX() - cluster2.getX()
        dir_y = cluster1.getY() - cluster2.getY()
        distance = numpy.sqrt( (dir_x)**2 + (dir_y)**2 )
        radius = cluster1.getR() + cluster2.getR()
        
        x = cluster1.getX() + (dir_x / distance) * radius
        y = cluster1.getY() + (dir_y / distance) * radius
        
        #return new position of cluster2
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
        
        