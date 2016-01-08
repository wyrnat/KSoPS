'''
Created on 19.10.2015

@author: jannik
'''
import numpy
from Services.calculationService import CalculationService
from scipy import integrate

class InteraktionService(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def findCorrelation(self, cluster_list):
        self.cluster_list.sort(key = lambda dist: dist[0], reverse = True)  # mass[i] >= mass[i+1]
        
        x_list = numpy.array([cluster.getX() for cluster in cluster_list])
        y_list = numpy.array([cluster.getY() for cluster in cluster_list])
        r_list = numpy.array([cluster.getREv() for cluster in cluster_list])
        hash_list = numpy.array([cluster.getHash() for cluster in cluster_list])
        destroy_list = []
        
        for j in range(len(cluster_list)-1):
            if j in destroy_list:
                continue
            
            x_square = (x_list[j] - x_list[j+1:])**2
            y_square = (y_list[j] - y_list[j+1:])**2
            dist_list = numpy.sqrt(x_square + y_square)

            destroy = (numpy.arange(len(dist_list)) + j + 1)[dist_list <= r_list[j] + r_list[j+1:]]
            
            for i in destroy:
                if i in destroy_list:
                    continue
                if self.cluster_list[i].m < self.cluster_list[i].m_0:
                    destroy_list.append(i)
                    continue
                flow, kill = self.cluster_list[j].absorb(self.cluster_list[i], self.A_aggregation*self.A_time_steps,
                                                         self.A_penetration_depth)
                if flow == 0:
                    pass
                elif  kill == False:
                    self.cluster_list[i].donate(self.cluster_list[j], flow)
                else:
                    destroy_list.append(hash_list[i])   

        self.cluster_list.removeParticle(destroy_list)
            
    @staticmethod        
    def getSputterOverlap(cluster_list1, cluster_list2):
        """
        @param cluster_list1: 
        """
        rev_result = []
        r_result = []
        x_list = numpy.array([cluster.getX() for cluster in cluster_list2.GET()])
        y_list = numpy.array([cluster.getY() for cluster in cluster_list2.GET()])
        r_list = numpy.array([cluster.getR() for cluster in cluster_list2.GET()])
        rev_list = numpy.array([cluster.getREv() for cluster in cluster_list2.GET()])
        hash_list = numpy.array([cluster.getHash() for cluster in cluster_list2.GET()])
        
        print cluster_list1.GET()
        for cluster in cluster_list1.GET():    
            x_square = (cluster.getX() - x_list)**2
            y_square = (cluster.getY() - y_list)**2
            distance_list = numpy.sqrt(x_square + y_square)
            print cluster.getREv()

            rev_result_part = (hash_list)[(distance_list <= cluster.getREv() + rev_list)]
            r_result_part = (hash_list)[(distance_list <= cluster.getR() + r_list)]
            
            for myhash in r_result_part:
                if myhash in rev_result_part:
                    j = numpy.where(rev_result_part == myhash)[0][0]
                    numpy.delete(rev_result_part, j, 0)
            
                
            rev_result.append(rev_result_part)
            r_result.append(r_result_part)
        return r_result, rev_result
            
        
    def checkGreatProhability(self, radius_ev1, radius_ev2, radius1, radius2, distance, steps1, steps2):
        func1 = CalculationService.dim2GaussFunction(radius_ev1, radius1, 0)
        func2 = CalculationService.dim2GaussFunction(radius_ev2, radius2, distance)
        
        dim1Overlap = lambda x: func1(0,x) * func2(0,x)
        x = (radius_ev1**2 - radius_ev2**2 + distance**2)/(2*distance)
        x_diff = radius_ev1 - x
        result = integrate.quad(dim1Overlap, x-x_diff, x+x_diff)
        if result >= 1:
            return True
        
        return False
        