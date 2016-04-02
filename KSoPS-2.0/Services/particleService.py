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
        
    def AdatomOnSurface(self, adatom, adatomList, adatomWWList, clusterList, coalescenceList):
        p = adatomList.removeParticle(adatom)
        if p != None:
            clusterList.addParticle(p)
            adatomWWList.addParticle(p)
            coalescenceList.addAdatom(p)
            
            
    def addAdatomtoCluster(self, initval, adatom, cluster, adatomList, clusterList):
        p = adatomList.removeParticle(adatom)
        if p != None:
            clusterList.addToParticle(cluster, 1)
            self.refreshCluster(initval, cluster)
            
    
    def adatomClusterWW(self, initval, adatom, cluster, adatomWWList, clusterList, coalescenceList):
        """
        Handles the adatoms who were deposited on the substrate
        They are within adatomWWList and ClusterList
        """
        p = adatomWWList.removeParticle(adatom)
        if clusterList.removeParticle(p) != None:
            cluster.atomFlow(1)
            coalescenceList.removeCluster(p)
            self.refreshCluster(initval, cluster, coalescenceList)
            
    def ClusterDiffusion(self, initval, pl):
        initServ = InitValService()
        rndm = random.random()
        G = numpy.random.normal(0,1/numpy.sqrt(12))
        n = pl.getInterN()
        r_ev = pl.GET()[0].getREv()
        if r_ev > 0.01:
            dx = r_ev * G * numpy.sin(2 * numpy.pi * rndm)
            dy = r_ev * G * numpy.cos(2 * numpy.pi * rndm)
            dx, dy = self.checkBorders(initval, pl, dx, dy)
            pl.moveAll(dx, dy)
            return True
        return False
    
    def fuseParticleLists(self, pl1, pl2):
        for particle in pl2.GET():
            pl1.addParticle(pl2.removeParticle(particle))
            
    def atomFlow(self, initval, cluster):
        initServ = InitValService()
        for adCluster in cluster.getContacts():
            if adCluster.getN()>cluster.getN():
                continue
            else:
                flow = initServ.getAtomFlow(initval, adCluster.getR())
                if adCluster.atomFlow(-1*flow) == True:
                    cluster.atomFlow(flow)
                else:
                    cluster.atomFlow(adCluster.getN())
                    adCluster.atomFlow(-1* adCluster.getN())
                    
    def deleteEmptyClusters(self, clusterList, coalescenceList):
        for cluster in clusterList.GET():
            if cluster.getN() == 0:
                clusterList.removeParticle()
                coalescenceList.removeCluster(cluster)
        coalescenceList.clearList()
        
    def clusterSurfaceTouching(self, cluster1, cluster2):
        """
        Move cluster2 to get in touch with the surface of cluster1
        """
        assert(cluster1 != cluster2), "particleService.clusterSurfaceTouching: particles identical"
        dir_x = cluster1.getX() - cluster2.getX()
        dir_y = cluster1.getY() - cluster2.getY()
        distance = numpy.sqrt( (dir_x)**2 + (dir_y)**2 )
        radius = cluster1.getR() + cluster2.getR()
        
        x = cluster2.getX() + dir_x * (distance - radius)/distance
        y = cluster2.getY() + dir_y * (distance - radius)/distance

        
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
        ndx = dx
        ndy = dy
        for cluster in pl.GET():
            dir_x = (cluster.getX()+ndx)/abs(cluster.getX()+ndx)
            if abs(cluster.getX() + ndx + cluster.getR()*dir_x) > area /2.:
                ndx = abs(area/2. - cluster.getX() -cluster.getR()*dir_x) * dx / abs(dx)
                
            dir_y = (cluster.getY()+ndy)/abs(cluster.getY()+ndy)
            if abs(cluster.getY() + ndy + cluster.getR()*dir_y) > area /2.:
                ndy = abs(area/2. - cluster.getY() -cluster.getR()*dir_y) * dy / abs(dy)
                
        return ndx , ndy
    
            
    def refreshCluster(self, initval, cluster, coalescenceList):
        self.setClusterR(initval, cluster)
        self.setInterfaceAtoms(initval, cluster)
        self.setClusterRev(initval, cluster, coalescenceList)
            
    def setClusterRev(self, initval, cluster, coalescenceList):
        """
        Gets the interface Atoms of the clusters
        associated with a coalescence group and
        calculates the event radius
        """
        initServ = InitValService()
        R = cluster.getR()
        liste = coalescenceList.findCluster(cluster)
        N = liste.getInterN()
        rev = initServ.getREv(initval, N)
        cluster.setREv( rev / numpy.power(3, N-1) + R )
        
    def setClusterR(self, initval, cluster):
        R = numpy.power(6*numpy.sqrt(2)/numpy.pi * cluster.getN(), 1/3.) * initval.getValue('radius')
        cluster.setR(R)
        
    def setInterfaceAtoms(self, initval, cluster):
        r = initval.getValue('radius')
        R = cluster.getR()
        cluster.setInterN(numpy.ceil( numpy.sqrt(2) * numpy.pi / 8. * R**2 / r**2 ))
        
    
    def setSurfaceAtoms(self, initval, cluster):
        r = initval.getR()
        R = cluster.getR()
        cluster.setSurfaceN( numpy.floor(numpy.pi/3./numpy.sqrt(2)*(6*R**2/r**2 - 12*R/r + 8)) )
    
        
    def addContact(self, cluster1, cluster2):
        """
        add the clusters to each others contact lists
        """
        if cluster2 in cluster1.getContacts():
            return False
        if cluster1.getN() < cluster2.getN():
            for adCluster in cluster1.getContacts():
                if adCluster.getN() > cluster1.getN():
                    return False
            cluster1.addContacts([cluster2])
            cluster2.addContacts([cluster1])
            return True
            
        elif cluster1.getN() > cluster2.getN():
            for adCluster in cluster2.getContacts():
                if adCluster.getN() > cluster2.getN():
                    return False
            cluster1.addContacts([cluster2])
            cluster2.addContacts([cluster1])
            return True
        
        else:
            isthebiggest = True
            for adCluster in cluster1.getContacts():
                if adCluster.getN() > cluster1.getN():
                    isthebiggest = False
                    break
            for adCluster in cluster2.getContacts():
                if adCluster.getN() > cluster2.getN() and isthebiggest == False:
                    return False
                
            cluster1.addContacts([cluster2])
            cluster2.addContacts([cluster1])
            return True
                    
    def getParticleDistance(self, cluster1, cluster2):
        dir_x = cluster1.getX() - cluster2.getX()
        dir_y = cluster1.getY() - cluster2.getY()
        return numpy.sqrt( (dir_x)**2 + (dir_y)**2 ) 
                
                
            #TODO: 2 cluster der selben groesse
            #for adCluster in cluster1.getContacts()
            
        
        
        
#     def setHoehe(self, R, partikel):
#         n = partikel.getDistLen()
#         h = n * R * sqrt3
#         partikel.setVektorVal(h, 5)
        
#     def setClusterRadius(self, R, partikel):
#         atoms = partikel.getDist()[0]
#         stacks = atoms / 6 + 1
#         if atoms == 1:
#             partikel.setR(R)
#         elif (stacks % 2) == 0:
#             partikel.setVektorVal(sqrt3 * R * stacks + R, 4)
#         elif (stacks % 2) == 1:
#             partikel.setVektorVal(R * numpy.sqrt(3*stacks**2 + 6*stacks + 1) + R)
        
#     def PrecheckDist(self, partikel, pos):
#         dist = partikel.getDist()
#         if pos < 0:
#             return False
#         if len(dist) <= pos:
#             return False
#         if pos == 0:
#             return True
#         if dist[pos] + 1 <= (dist[pos-1]-1)/2:
#             return True
#         return False
        
    

        
    
#     def addAtoms(self, partikel, pos, number=1):
#         if pos < 0:
#             pos = partikel.getDistLen() + pos
#         for i in range(number):
#             new_pos = pos    
#             while self.PrecheckDist(partikel, new_pos) == False:
#                 new_pos -= 1
#             n = partikel.getDist(new_pos)
#             partikel.setDistVal(n+1, new_pos)
#             
#     def removeAtom(self, partikel, pos):
#         partikel.setDistVal()
#             
#     def atomFlow(self, partikel, number):
#         dist = partikel.getDist()
#         n = partikel.getn()
#         if number >= 0:
#             dist[0] += number
#         else:
#             pass
        
        
        
        
        
        
        
        
        