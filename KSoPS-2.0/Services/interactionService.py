'''
Created on 19.10.2015

@author: jannik
'''
import numpy
from scipy import integrate
from particleService import ParticleService
from random import random

class InteractionService(object):
    '''
    classdocs
    '''

        
    def adatomOnCluster(self, initval, adatomList, adatomWWList, clusterList, coalescenceList, smeasure):
        pServ = ParticleService()
        
        x_list = numpy.array([cluster.getX() for cluster in clusterList.GET()])
        y_list = numpy.array([cluster.getY() for cluster in clusterList.GET()])
        r_list = numpy.array([cluster.getR() for cluster in clusterList.GET()])
        
        for adatom in adatomList.GET():
            x_square = (adatom.getX() - x_list)**2
            y_square = (adatom.getY() - y_list)**2
            distance_list = numpy.array(numpy.sqrt(x_square + y_square))
            
            
            cluster = (numpy.array(clusterList.GET()))[distance_list <= (adatom.getR() + r_list)]
            if len(cluster)!=0:
                pServ.addAdatomtoCluster(initval, adatom, cluster, adatomList, clusterList)
                smeasure.adatomEvent('clusterdeposition_sputter', 1)
            else:
                pServ.AdatomOnSurface(adatom, adatomList, adatomWWList, clusterList, coalescenceList)
                smeasure.adatomEvent('deposition_sputter', 1)
                
    def adatomWW(self, initval, adatomWWList, clusterList, coalescenceList, smeasure):
        pServ = ParticleService()
        
        x_list = numpy.array([cluster.getX() for cluster in clusterList.GET()])
        y_list = numpy.array([cluster.getY() for cluster in clusterList.GET()])
        r_list = numpy.array([cluster.getR() for cluster in clusterList.GET()])
        rev_list = numpy.array([cluster.getREv() for cluster in clusterList.GET()])
        
        for adatom in adatomWWList.GET():
            x_square = (adatom.getX() - x_list)**2
            y_square = (adatom.getY() - y_list)**2
            distance_list = numpy.array(numpy.sqrt(x_square + y_square))
            
            r_ol = (numpy.array(clusterList.GET()))[(distance_list <= adatom.getR() + r_list)]
            rev_ol = (numpy.array(clusterList.GET()))[(distance_list <= adatom.getREv() + rev_list)]
            
            ''' *** R Overlap *** '''
            r_ol=numpy.delete(r_ol, numpy.where(r_ol==adatom)[0][0])
            if len(r_ol) != 0:
                pServ.adatomClusterWW(initval, adatom, r_ol[0], adatomWWList, clusterList, coalescenceList)
                if r_ol[0].getN() == 1:
                    smeasure.adatomEvent('nucleation',1)
                else:
                    smeasure.adatomEvent('aggregation',1)
                continue

            ''' *** Rev Overlap for great WQS *** '''
            rev_ol=numpy.delete(rev_ol, numpy.where(rev_ol==adatom)[0][0])
            interaction = False
            if len(rev_ol) != 0:
                for cluster in rev_ol:
                    distance = self.getParticleDistance(adatom.getX(), adatom.getY(), cluster.getX(), cluster.getY())
                    if self.checkGreatProhability(adatom.getREv(), cluster.getREv(), adatom.getR(), cluster.getR(), distance) >= 1:
                        pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList)
                        if cluster.getN() == 1:
                            smeasure.adatomEvent('nucleation',1)
                        else:
                            smeasure.adatomEvent('aggregation',1)
                        interaction = True
                        break
                
                ''' *** Rev Overlap for small WQS *** '''
                if interaction == False:
                    for cluster in rev_ol:
                        distance = self.getParticleDistance(adatom.getX(), adatom.getY(), cluster.getX(), cluster.getY())
                        WQS = self.getCollisionProhability(adatom.getREv(), cluster.getREv(), adatom.getR(), cluster.getR(), distance)
                        if random() < WQS:
                            pServ.adatomClusterWW(initval, adatom, cluster, adatomWWList, clusterList, coalescenceList)
                            if cluster.getN() == 1:
                                smeasure.adatomEvent('nucleation',2)
                            else:
                                smeasure.adatomEvent('aggregation',1)
                            interaction = True
                            break
                        
    def diffusionOverlap(self, initval, pl, clusterList, coalescenceList):
        pServ = ParticleService()
        
        x_list = numpy.array([cluster.getX() for cluster in clusterList.GET()])
        y_list = numpy.array([cluster.getY() for cluster in clusterList.GET()])
        r_list = numpy.array([cluster.getR() for cluster in clusterList.GET()])
        rev_list = numpy.array([cluster.getREv() for cluster in clusterList.GET()])
        
        for cluster in pl.GET():
            x_square = (cluster.getX() - x_list)**2
            y_square = (cluster.getY() - y_list)**2
            distance_list = numpy.sqrt(x_square + y_square)
            
            r_ol = (numpy.array(clusterList.GET()))[(distance_list <= cluster.getR() + r_list)]
            rev_ol = (numpy.array(clusterList.GET()))[(distance_list <= cluster.getREv() + rev_list)]
            

            r_ol_clear = [cluster for cluster in r_ol if cluster not in pl.GET()]
            
            if len(r_ol_clear) != 0 and coalescenceList.findCluster(r_ol_clear[0])!=None:
                fuse=False
                for cluster2 in r_ol_clear:
                    if pServ.addContact(cluster, cluster2):
                        pServ.fuseParticleLists(coalescenceList.findCluster(cluster2), pl)
                        fuse=True
                        break
            
            rev_ol_clear = [cluster for cluster in rev_ol if (cluster not in pl.GET() and cluster not in r_ol_clear)]
            
            if len(rev_ol_clear) != 0 and coalescenceList.findCluster(r_ol_clear[0])!=None and fuse==False:
                for cluster2 in rev_ol_clear:
                    distance = self.getParticleDistance(cluster.getX(), cluster.getY(), cluster2.getX(), cluster2.getY())
                    if self.checkGreatProhability(cluster.getREv(), cluster2.getREv(), cluster.getR(), cluster2.getR(), distance) >= 1:
                        if pServ.addContact(cluster, cluster2):
                            pServ.fuseParticleLists(coalescenceList.findCluster(cluster2),pl)
                    else:
                        WQS = self.getCollisionProhability(cluster2.getREv(), cluster.getREv(), cluster2.getR(), cluster.getR(), distance)
                        rndm = random.random
                        if rndm < WQS:
                            if pServ.addContact(cluster, cluster2):
                                pServ.fuseParticleLists(coalescenceList.findCluster(cluster2),pl)
                                
    def calibrateCluster(self, pl):
        partServ = ParticleService()
        x_list = numpy.array([cluster.getX() for cluster in pl.GET()])
        y_list = numpy.array([cluster.getY() for cluster in pl.GET()])
        r_list = numpy.array([cluster.getR() for cluster in pl.GET()])
        
        for cluster in pl.GET():
            x_square = (cluster.getX() - x_list)**2
            y_square = (cluster.getY() - y_list)**2
            distance_list = numpy.sqrt(x_square + y_square)
            
            r_ol = (numpy.array(pl.GET()))[(distance_list <= cluster.getR() + r_list)]
            r_ol_clear = [elm for elm in r_ol if (elm not in cluster.getContacts()) and (elm != cluster)]
            
            for interCluster in r_ol_clear:
                if interCluster.getN() > cluster.getN():
                    continue
                else:
                    partServ.clusterSurfaceTouching(cluster, interCluster)
            
            for adCluster in cluster.getContacts():
                if adCluster.getN() > cluster.getN():
                    continue
                else:
                    partServ.clusterSurfaceTouching(cluster, adCluster)     
                    
    def findClosestCluster(self, cluster, clusterList):
        temp_liste = clusterList.GET()
        temp_liste.remove(cluster)
        x_list = numpy.array([particle.getX() for particle in temp_liste])
        y_list = numpy.array([particle.getY() for particle in temp_liste])
        distance_list = numpy.sqrt( (cluster.getX()-x_list)**2 + (cluster.getY()-y_list)**2 )   
        return numpy.amin(distance_list)
            
            
        
            
            
            
    
    def findCorrelation(self, cluster_list, clustercluster_hashlist_list):
        """
        
        """
        #sort for particle number
        self.cluster_list.sort(key = lambda dist: dist[0], reverse = True)  # mass[i] >= mass[i+1]
        
        x_list = numpy.array([cluster.getX() for cluster in cluster_list])
        y_list = numpy.array([cluster.getY() for cluster in cluster_list])
        r_list = numpy.array([cluster.getREv() for cluster in cluster_list])
        hash_list = numpy.array([cluster.getHash() for cluster in cluster_list])
        destroy_list = []            
        
        for j in range(len(cluster_list)-1):
            if j.getHash() in destroy_list:
                continue
            
            x_square = (x_list[j] - x_list[j+1:])**2
            y_square = (y_list[j] - y_list[j+1:])**2
            dist_list = numpy.sqrt(x_square + y_square)

            destroy = (numpy.arange(len(dist_list)) + j + 1)[dist_list <= r_list[j] + r_list[j+1:]]
            
            
            
            for i in destroy:
                if i in destroy_list:
                    continue
                
                same_clusterclusterlist = False
                for hashlist in clustercluster_hashlist_list:
                    if (cluster_list[i].getHash() in hashlist) and ((cluster_list[j].getHash() in hashlist)):
                        same_clusterclusterlist = True
                        break
                    if (cluster_list[i].getHash() in hashlist) and ((cluster_list[j].getHash() not in hashlist)):
                        break
                    if (cluster_list[i].getHash() not in hashlist) and ((cluster_list[j].getHash() in hashlist)):
                        break
                if same_clusterclusterlist == True:
                    continue
                
                else:
                    destroy_list.append(hash_list[i])   

        self.cluster_list.removeParticle(destroy_list)
                    
    def getSputterOverlap(self, cluster_list1, cluster_list2):
        """
        @param cluster_list1: 
        """
        rev_result = []
        r_result = []
        x_list = numpy.array([cluster.getX() for cluster in cluster_list2.GET()])
        y_list = numpy.array([cluster.getY() for cluster in cluster_list2.GET()])
        r_list = numpy.array([cluster.getR() for cluster in cluster_list2.GET()])
        rev_list = numpy.array([cluster.getREv() for cluster in cluster_list2.GET()])
        
        for cluster in cluster_list1.GET():    
            x_square = (cluster.getX() - x_list)**2
            y_square = (cluster.getY() - y_list)**2
            distance_list = numpy.sqrt(x_square + y_square)

            rev_result_part = (cluster_list2.GET())[(distance_list <= cluster.getREv() + rev_list)]
            r_result_part = (cluster_list2.GET())[(distance_list <= cluster.getR() + r_list)]
            
            #delete hash_list entries in rev_result for existing in r
            rev_result_part = [x for x in rev_result_part if x not in r_result_part]   
             
            rev_result.append(rev_result_part)
            r_result.append(r_result_part)
        return r_result, rev_result
    
            
    def dim2GaussFunction(self, radius_ev, radius, r_0):
        # diffusion length / sqrt(12)
        sigma = (radius_ev - radius)/3.464
        
        #round value to prevent overflow 
        if sigma < 0.001:
            #define a step function
            result = lambda y,x: (abs(numpy.sqrt(y**2+(x-r_0)**2)) < radius)*1.0
            return result
        else:
            c = numpy.sqrt(2*numpy.pi)
            
            #define the gauss function in 1dim. with 2dim normalisation
            dist = lambda r: numpy.exp(-(r/sigma)**2/2.) / c**2 / sigma**2
            
            #calculate the gauss with integration over the sphere
            dist_int = lambda r: (integrate.quad(dist, r-radius, r+radius))[0]
            
            result = lambda y,x: dist_int(numpy.sqrt(y**2+(x-r_0)**2))
        
            #returns a 2dim sphere integrated gauss function depending on y,x
            return result
        
        
            
    def normalDistributionIntegration(self, radius_ev, radius, position):
        # diffusion length / sqrt(12)
        sigma = (radius_ev - radius)/3.464
        
        #round value to prevent overflow 
        if sigma < 0.001:
            return 1
        
        a = position - radius
        b = position + radius
        
        c = numpy.sqrt(2*numpy.pi)
        gauss = lambda x: numpy.exp(-(x/sigma)**2/2) / c / sigma
        result = integrate.quad(gauss, a, b)
        return result[0]
    

    def getCollisionProhability(self, radius_ev1, radius_ev2, radius1, radius2, distance):
        func1 = self.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = self.dim2GaussFunction(radius_ev2, radius2, distance)
        
        
        #If R_ev ~= R
        if func1(0,0) == func1(0,radius_ev1/2.):
            highfun = lambda x: numpy.sqrt(radius1**2-x**2)
            lowfun = lambda x: -highfun(x)
            prohability = integrate.dblquad(func2, -radius1, radius1,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
            return prohability[0]
        
        elif func2(0,0) == func2(0,radius_ev2/2.):
            highfun = lambda x: numpy.sqrt(radius2**2-(x-distance)**2)
            lowfun = lambda x: -highfun(x)
            prohability = integrate.dblquad(func1, distance-radius2, distance+radius2,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
            return prohability[0]
        
        else:
            #defines the overlap of both prohability functions
            overlap = lambda y,x: func1(y,x) * func2(y,x)
            
            x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
            x_diff = radius_ev1 - x
            y_diff = numpy.sqrt(radius_ev1**2-x**2)
            
            
            lowfun = lambda x: -y_diff
            highfun = lambda x: y_diff
        
            prohability = integrate.dblquad(overlap, x-x_diff, x+x_diff,
                                            lowfun, highfun,
                                            epsabs=0.01, epsrel=0.01)
        
            return prohability[0]
        
    def checkGreatProhability(self, radius_ev1, radius_ev2, radius1, radius2, distance):
        """
        estimate if the overlap integral of the prohability density functions of two clusters
        is greater than 1 to shorten calculation time.
        Make a cut along the centers of the event radii and integrate it
        """
        func1 = self.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = self.dim2GaussFunction(radius_ev2, radius2, distance)
        
        dim1Overlap = lambda x: func1(0,x) * func2(0,x)
        
        #overlap cross section of event radii
        x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
        x_diff = radius_ev1 - x
        result = integrate.quad(dim1Overlap, x-x_diff, x+x_diff)
        return result
    
    def getParticleDistance(self, x1, y1, x2, y2):
        return numpy.sqrt((x1-x2)**2+(y1-y2)**2)
           
        
            
        