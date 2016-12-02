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
    


    def __init__(self, initval, size = 800):
        '''
        Constructor
        '''
        pygame.init()
        self.fontsize = int(size/20)
        self.myfont = pygame.font.SysFont("monospace", self.fontsize, bold=True)
        self.area = initval.getValue('area')
        self.mult = numpy.round(size/(self.area))
        self.screen = pygame.display.set_mode((self.area*self.mult,self.area*self.mult))
        self.thickness = initval.getValue('growth_rate')
        
        stepsize = initval.getValue('step_size')
        measuresteps = initval.getValue('measure_steps')
        self.thickness_var = int(-numpy.log10(self.thickness*stepsize*measuresteps))
        self.time_var = int(-numpy.log10(stepsize*measuresteps/1000.))
        
    def draw(self, cluster_plist, time, thickness, step):
        self.screen.fill(black)


        for values in cluster_plist[step]:
            x = values[0]
            y = values[1]
            r = values[2]
            rev = values[3]
            N = values[4]
            
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
            #label = self.myfont.render(str(N), 1, (0,255,0))
            #self.screen.blit(label,(int(numpy.ceil(x*self.mult) + self.area*self.mult/2. - self.fontsize/2.), int(numpy.ceil(y*self.mult + self.area*self.mult/2. - self.fontsize/2.))))
        thick_label = "Thickness: "+str(numpy.round(thickness, self.thickness_var))+"nm"
        time_label = "Time: "+str(numpy.round(time, self.time_var))+"s"
        label1 = self.myfont.render(thick_label, 1, (0,255,0))
        label2 = self.myfont.render(time_label, 1, (0,255,0))
        self.screen.blit(label1, (int(0.01*self.area*self.mult), int(0.01*self.area*self.mult)))
        self.screen.blit(label2, (int(0.01*self.area*self.mult), int(0.01*self.area*self.mult + self.fontsize +1)))  
        pygame.display.flip()

    def kill(self):
        pygame.display.quit()
        
    def safeImage(self, myfilename, step):
        number = ("0")*(step<10)+("0")*(step<100)+("0")*(step<1000)+("0")*(step<10000)+str(step)
        pygame.image.save(self.screen, myfilename+"_"+number+".jpg")