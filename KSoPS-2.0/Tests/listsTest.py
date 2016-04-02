'''
Created on 30.03.2016

@author: jannik
'''

from Materialien.particleList import ParticleList
from Fachwerte.particle import Particle

mylist = ParticleList()
for i in range(5):
    mylist.addParticle(Particle(1,1,1,1))
    
a = mylist.GET()
a.pop(2)
a.pop(1)

b = mylist.GET()

print mylist.GET()
print a == b