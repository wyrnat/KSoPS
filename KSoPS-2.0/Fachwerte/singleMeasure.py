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
        self.adatom = {'deposition_sputter': 0,
                       'clusterdeposition_sputter': 0,
                       'nucleation': 0,
                       'aggregation': 0,
                       'coalescence': 0
                       }
        
        
    def adatomEvent(self, param, val):
        if param in self.adatom:
            self.adatom[param] += val
            
    def getadatomEvent(self, param):
        if param in self.adatom:
            return self.adatom[param]
        return None
    
    def GET(self):
        return list(self.adatom)