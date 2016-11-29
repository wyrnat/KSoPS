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
        self.mult = numpy.round(800/(self.area))
        self.screen = pygame.display.set_mode((self.area*self.mult,self.area*self.mult))
        
    def draw(self, initval, cluster_plist, step):
        self.screen.fill(black)

        for values in cluster_plist[step]:
            x = values[0]
            y = values[1]
            r = values[2]
            rev = values[3]
            N = values[4]
            masterN = values[5]
            
            if N == 1:
                color = gold
            else:
                color = white
                
                
            pygame.draw.circle(self.screen,
                                color,
                                (int(numpy.ceil(x*self.mult + self.area*self.mult/2.)), int(numpy.ceil(y*self.mult + self.area*self.mult/2.)) ),
                                int(numpy.ceil(r*self.mult))
                               )
            pygame.draw.circle(self.screen,
                               red,
                               (int(numpy.ceil(x*self.mult) + self.area*self.mult/2.), int(numpy.ceil(y*self.mult + self.area*self.mult/2.))),
                               int(numpy.ceil(rev*self.mult)),
                               1
                               ) 
            label = self.myfont.render(str(N)+";"+str(masterN), 1, (0,255,0))
            self.screen.blit(label,(int(numpy.ceil(x*self.mult) + self.area*self.mult/2. - r*self.mult/2.), int(numpy.ceil(y*self.mult + self.area*self.mult/2. - r*self.mult/2.))))
            
        pygame.display.flip()

    def kill(self):
        pygame.display.quit()