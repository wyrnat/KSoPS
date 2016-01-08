'''
Created on 04.11.2015

@author: jannik
'''
from Fachwerte.messungen import Messungen

class MessungenService(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.messungen = Messungen()
        self.dist_ww = [0,0,0] # [deposition, nucleation, aggregation]
        
    def auswerteParameter(self, partikelListe, clusterListe):
        #TODO: Entnehme die Werte den Listen und uebergebe sie an eine Instanz von Messungen
        pass
    
    def newDeposition(self, n):
        self.dist_ww[0] += n
        
    def newNucleation(self, n):
        self.dist_ww[1] += n
        
    def newAggregation(self, n):
        self.dist_ww[2] += n