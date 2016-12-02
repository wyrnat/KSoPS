'''
Created on 01.12.2016

@author: jannik
'''
import numpy

n = 100000
R = numpy.power(2 * 1 * n, 1/3.) * 0.1
print "R: "+str(R)
n_s = 1 * ( 3*(R/0.1)**2 - 6*R/0.1 + 4)

print "ns: "+str(n_s)