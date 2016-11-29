'''
Created on 21.03.2016

@author: jannik
'''

class SingleMeasure(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.adatom = {'deposition_sputter': 0,        #deposition on substrate
                       'clusterdeposition_sputter': 0, #deposistion on cluster
                       'nucleation': 0,                #2 adatoms
                       'aggregation': 0,               #adatom and cluster
                       'coalescence': 0                #2 clusters
                       }
        
        
    def adatomEvent(self, param, val):
        assert (param in self.adatom), "adatomEvent: param not a valid event"
        self.adatom[param] += val
            
    def getadatomEvent(self, param):
        if param in self.adatom:
            return self.adatom[param]
        return None
    
    def GET(self):
        return self.adatom