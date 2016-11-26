'''
Created on 15.10.2015

@author: Jannik Woehnert
'''

import random
import numpy
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
        if p != None:
            clusterList.addParticle(p)
            #adatomWWList.addParticle(p)
            coalescenceList.addAdatom(p)
            
            
    def addAdatomtoCluster(self, initval, adatom, cluster, adatomList, clusterList, coalescenceList): 
        if adatomList.removeParticle(adatom):
            cluster.atomFlow(1)
            self.refreshCluster(initval, cluster, coalescenceList)
            
    def addParticleToCluster(self, initval, particle, cluster, clusterList, coalescenceList):
        assert (particle in clusterList.GET()), "addparticleToCluster: particle not in particlelist"
        assert (cluster in clusterList.GET()), "addparticleToCluster: cluster not in particlelist"
        clusterList.removeParticle(particle)
        coalescenceList.removeCluster(particle)
        cluster.atomFlow(particle.getN())
        self.refreshCluster(initval, cluster, coalescenceList)

            
    """ Adatom WW """        
            
    def adatomClusterWW(self, initval, adatom, cluster, adatomWWList, clusterList, coalescenceList):
        """
        Handles the adatoms who were deposited on the substrate
        They are within adatomWWList and ClusterList
        """
        if (cluster in clusterList.GET()) and (clusterList.removeParticle(adatom) != None):
            adatomWWList.removeParticle(adatom)
            cluster.atomFlow(1)
            coalescenceList.removeCluster(adatom)
            self.refreshCluster(initval, cluster, coalescenceList)
            return True
        return False
    
    
    
    
    
    
    
    """ Diffusion """
            
    def ClusterDiffusion(self, initval, pl):
        if pl.clusterNumber() == 0:
            return False
        
        initServ = InitValService()
        rndm = random.random()
        #create Gaussian
        G = numpy.random.normal(0,1/numpy.sqrt(12))      
        move = pl.GET()[0].getREv() - pl.GET()[0].getR()
        
        #if movement is significant
        if move > initval.getValue('radius'):
            dx = move * G * numpy.sin(2 * numpy.pi * rndm)
            dy = move * G * numpy.cos(2 * numpy.pi * rndm)
            dx, dy = self.checkBorders(initval, pl, dx, dy)
            pl.moveAll(dx, dy)
            return True
        #otherwise check only for particle on area
        else:
            dx, dy = self.checkBorders(initval, pl, 0,0)
            pl.moveAll(dx,dy)
            return False
    
    def fuseParticleLists(self, pl1, pl2, coalescenceList):
        assert (pl1 in coalescenceList.GET()), "fuseparticleLists: pl1 not in coalescenceList"
        assert (pl2 in coalescenceList.GET()), "fuseparticleLists: pl2 not in coalescenceList"
        for particle in pl2.GET():
            pl1.addParticle(pl2.removeParticle(particle))
        coalescenceList.removePl(pl2)
            
    def atomFlow(self, initval, cluster, clusterList):
        initServ = InitValService()
        for adCluster in cluster.getContacts():
            if adCluster not in clusterList.GET():
                print "CLUSTERlist FAIL!"
                cluster.removeContacts([adCluster])
                continue
            if adCluster.getN()>cluster.getN():
                continue
            else:
                flow = initServ.getAtomFlow(initval, adCluster.getR())
                print "partileService.atomflow flow " + str(flow)
                if flow == 0:
                    continue
                elif adCluster.getN()>flow:
                    cluster.atomFlow(flow)
                    adCluster.atomFlow(-1*flow)
                else:
                    cluster.atomFlow(adCluster.getN())
                    adCluster.atomFlow(-1* adCluster.getN())
                    
                    adCluster.removeContacts([cluster])
                    adClusterContacts = adCluster.getContacts()
                    cluster.removeContacts([adCluster])
                    cluster.addContacts(adClusterContacts)
                    for contact in adClusterContacts:
                        contact.removeContacts([adCluster])
                        contact.addContacts([cluster])
                    
    def deleteEmptyClusters(self, clusterList, coalescenceList):
        for cluster in clusterList.GET():
            if cluster.getN() == 0:
                clusterList.removeParticle(cluster)
                coalescenceList.removeCluster(cluster)
                for contact in cluster.getContacts():
                    contact.removeContacts([cluster])
        coalescenceList.clearList()
        
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

        
        cluster2.setX( x )
        cluster2.setY( y )
        
    def getFusedREv(self, initval, pl):
        initServ = InitValService()
        N = pl.getInterN()
        return initServ.getREv(initval, N)
            
    
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
    
    def getParticleDistance(self, cluster1, cluster2):
        dir_x = cluster1.getX() - cluster2.getX()
        dir_y = cluster1.getY() - cluster2.getY()
        return numpy.sqrt( (dir_x)**2 + (dir_y)**2 ) 
    
            
    def refreshCluster(self, initval, cluster, coalescenceList):
        self.setClusterR(initval, cluster)
        self.setSurfaceAtoms(initval, cluster)
        self.setClusterRev(initval, cluster, coalescenceList)
            
    def setClusterRev(self, initval, cluster, coalescenceList):
        """
        Gets the interface Atoms of the clusters
        associated with a coalescence group and
        calculates the event radius
        """
        assert (coalescenceList.findCluster(cluster) != None), str(cluster) + " not in coalescenceList"
        
        initServ = InitValService()
        R = cluster.getR()
        liste = coalescenceList.findCluster(cluster)
        N = liste.getAllN()
        rev = initServ.getREv(initval, N)
        if rev > initval.getValue('radius'):
            cluster.setREv( rev + R )
        else:
            cluster.setREv(R)
    

    def setClusterR(self, initval, cluster):
        if cluster.getN() < 2:
            R = initval.getValue('radius')
        else:
            R = numpy.power(6*numpy.sqrt(2)/numpy.pi * cluster.getN(), 1/3.) * initval.getValue('radius')
        cluster.setR(R)        
    
    def setSurfaceAtoms(self, initval, cluster):
        r = initval.getR()
        R = cluster.getR()
        N = cluster.getN()
        if N>12:
            cluster.setSurfaceN( numpy.floor(numpy.pi/3./numpy.sqrt(2)*(6*R**2/r**2 - 12*R/r + 8)) )
        else:
            cluster.setSurfaceN(N)
        
    def addContact(self, cluster1, cluster2):
        
        if cluster1.getN()>cluster2.getN():
            if cluster2.getMaster() != None:
                cluster1.setMaster(cluster2)
                return True
            else:
                return False
                 
    
        
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
        
        