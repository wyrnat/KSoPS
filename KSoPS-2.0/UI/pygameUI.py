'''
Created on 04.04.2016

@author: jannik
'''
import pygame
import numpy

black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)
red = (255,0,0)

class PygameUI(object):
    '''
    classdocs
    '''
    


    def __init__(self, initval):
        '''
        Constructor
        '''
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 15)
        self.area = initval.getValue('area')
        self.mult = 100
        self.screen = pygame.display.set_mode((self.area*self.mult,self.area*self.mult))
        
    def draw(self, initval, measurement, step):
        self.screen.fill(black)

        for values in measurement.getClusterProperties()[step]:
            
            if values[2] == initval.getValue('radius'):
                color = gold
            else:
                color = white
                
                
            pygame.draw.circle(self.screen,
                                color,
                                (int(numpy.round(values[0]*self.mult + self.area*self.mult/2.)), int(numpy.round(values[1]*self.mult + self.area*self.mult/2.)) ),
                                int(numpy.ceil(values[2]*self.mult))
                               )
            pygame.draw.circle(self.screen,
                               red,
                               (int(numpy.round(values[0]*self.mult) + self.area*self.mult/2.), int(numpy.round(values[1]*self.mult + self.area*self.mult/2.))),
                               int(numpy.floor(values[3]*self.mult)),
                               1
                               ) 
            label = self.myfont.render(str(values[4])+";"+str(values[5]), 1, (0,255,0))
            self.screen.blit(label,(int(numpy.round(values[0]*self.mult) + self.area*self.mult/2. - values[2]*self.mult/2.), int(numpy.round(values[1]*self.mult + self.area*self.mult/2. - values[2]*self.mult/2.))))
            
        pygame.display.flip()

    def kill(self):
        pygame.display.quit()