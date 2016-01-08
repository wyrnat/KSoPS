'''
Created on 10.12.2015

@author: jannik
'''

from Services.calculationService import CalculationService as cServ

#print cServ.normalDistributionIntegration(1.01, 1, 1.01)

func = cServ.dim2GaussFunction(2, 1, 2)

print func(0,0)
print func(0,0.5)
print func(0,1)
print func(1,0)
print func(1,1)
print "result:..."
print cServ.getCollisionProhability(radius_ev1=2.5, radius_ev2=2.5, radius1=2.5, radius2=0.144, distance=1.5)


