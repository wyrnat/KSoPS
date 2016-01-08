'''
Created on 22.10.2015

@author: jannik
'''

#TODO: rw Modus trennen, da Probleme bei nicht-existenten Dateien


import random
import os
import numpy

""" ***** Methods ****** """
def loadFileToList(gpath):
    result = []
    if os.path.exists(gpath):
        f = open(gpath, 'r')
        lines = f.readlines()
        for line in lines:
            value_str = line.split(";")[1]
            value = int(value_str)
            result.append(value)
        f.close()
        return result
    else:
        f = open(gpath, 'w')
        f.write("0 ; 0\n")
        f.close()
        return [0]
    
def writeListToFile(gpath, mylist):
    f = open(gpath, 'w')
    for i, value in enumerate(mylist):
        f.write(str(i)+" ; "+str(value)+"\n")
    f.close()
    
def nabs(val):
    return int(numpy.sqrt(val[0]**2 + val[1]**2 + val[2]**2)+0.5)
    
    
""" ****** Calculation ****** """

#start value
data_rows = 1000
step_array = [100, 200, 500, 800, 1000, 2000, 10000]
messungsnummer = 1 # If measures shall not be mixed
dim = 1 #in how many dimensions can the particle move
"""terms: [propability for this dimension, prop. for back step, prop. for front step]"""
wqs = [[1/3., 0.5, 0.5], [1/3., 0.5, 0.5], [1/3., 0.5, 0.5]]

#finals
mypath = os.getcwd() + "/Tests/" + "dim" + str(dim) + "/Run" + str(messungsnummer) + "/"
if not os.path.isdir(mypath):
    os.makedirs(mypath)


# For an array of different step counts
for l in range(data_rows):
    for n in step_array:
    
        #variables
        pos = [0, 0, 0] # 3dim free movement
        result_array = [1] # We start at position zero
        final_pos = None #measures the final position to save
        direction = 0
        name_dist = "Dist_" + str(n) + "steps.txt"
        name_final = "Final_" + str(n) + "steps.txt"
    
        # Every step of the total number of steps
        for i in range(n):
            dim_check = random.random()
            pm = random.random()
            if dim == 1:
                mysum = wqs[0][1] + wqs[0][2]
                if pm > wqs[0][1]/(mysum * 1.0):
                    pos[0] += 1
                if pm < wqs[0][1]/(mysum * 1.0):
                    pos[0] -= 1
            if dim == 2:
                dim_sum = wqs[1][0] + wqs[2][0]
                chdim = dim_check < wqs[1][0]/(dim_sum*1.0)
                mysum = wqs[chdim][1] + wqs[chdim][2]
                if pm > wqs[chdim][1]/(mysum*1.0):
                    pos[0] += 1
                if pm < wqs[chdim][1]/(mysum*1.0):
                    pos[0] -= 1
            
            final_pos = nabs(pos)
            if final_pos in range(len(result_array)):
                result_array[final_pos] += 1 + (final_pos == 0)
            else:
                result_array.append(1)
    
        
    # Messe den Endwert nach n Schritten
        prevList = loadFileToList(mypath+name_final)
        while len(prevList) <= final_pos:
            a = len(prevList)
            prevList.append(0) 
        prevList[final_pos] += 1 + (final_pos == 0)
        writeListToFile(mypath+name_final, prevList)
    
        # Messe die Verteilung fuer alle Schritte
        prevList = loadFileToList(mypath+name_dist)
        while len(prevList) <= len(result_array):
            a = len(prevList)
            prevList.append(0)
        for i, elem in enumerate(result_array):
            prevList[i] += elem
        writeListToFile(mypath+name_dist, prevList)
    
    print "Finished! Data Row #" + str(l)
print "*************************"   