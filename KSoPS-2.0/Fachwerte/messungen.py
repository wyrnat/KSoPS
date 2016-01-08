'''
Created on 19.10.2015

@author: jannik
'''
import numpy

class Messungen(object):
    '''
    classdocs
    '''
    """
    TODO speichere nur die grundlegenden Werte,
    der Rest wird beim getter Aufruf berechnet
    """
    


    def __init__(self):
        '''
        Constructor
        '''
        self.thickness = []
        self.radius = []
        self.distance = []
        self.height = []
        self.r_list = []
        self.d_list = []
        self.h_list = []
        self.cover = []
        self.island_density = []
        self.dist_ww = []
        self.radius_model = []
        self.distance_model = []
        self.height_model =[]
        
    def speichere(self, thickness, radius, distance, height, r_list, d_list,
                 h_list, cover, island_density, dist_ww,
                 radius_model, distance_model, height_model):
        
        assert (type(thickness) == float), "messung.speichere: thickness nicht float"
        assert (type(radius) == float), "messung.speichere: radius nicht float"
        assert (type(distance) == float), "messung.speichere: distance nicht float"
        assert (type(height) == float), "messung.speichere: height nicht float"
        assert (type(r_list) == list), "messung.speichere: r_list nicht list"
        assert (type(d_list) == list), "messung.speichere: d_list nicht list"
        assert (type(h_list) == list), "messung.speichere: h_list nicht list"
        assert (type(cover) == float), "messung.speichere: cover nicht float"
        assert (type(island_density) == float), "messung.speichere: island_density nicht float"
        assert (type(dist_ww) == list), "messung.speichere: dist_ww nicht list"
        assert (type(radius_model) == float), "messung.speichere: radius_model nicht float"
        assert (type(distance_model) == float), "messung.speichere: distance_model nicht float"
        assert (type(height_model) == float), "messung.speichere: height_model nicht float"
        
        self.thickness.append(thickness)
        self.radius.append(radius)
        self.distance.append(distance)
        self.height.append(height)
        self.r_list.append(r_list)
        self.d_list.append(d_list)
        self.h_list.append(h_list)
        self.cover.append(cover)
        self.island_density.append(island_density)
        self.dist_ww.append(dist_ww)
        self.radius_model.append(radius_model)
        
    def getThickness(self, index):
        return self.thickness[index]
    
    def getRadius(self, index):
        pass
        
    def getIndexWithThickness(self, thethickness):
        #if (thethickness < 0) or (thethickness > self.thickness[-1]):
        #    return None
        difference = abs(thethickness - numpy.array(self.thickness))
        min_diff = min(difference)
        result = difference.index(min_diff)
        return result
    
    
        
        
        
              
    
        