'''
Created on 05.11.2015

@author: jannik
'''

from Fachwerte import partikel
from Services import internService
service = internService.InternService()

p1 = partikel.Partikel(0,0,1,1,1, None, 0, [1,0])

print p1.getDist()

for i in range(100):
    service.addAtoms(p1, -1, 2)
    print p1.getDist()