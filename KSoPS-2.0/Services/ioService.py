'''
Created on 02.03.2016

@author: jannik
'''
import h5py

class IOService(object):
    '''
    Save and load data files
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    def saveAsHDF5(self, measure, file_name):
        myfile = h5py.File(file_name, "w")
        myfile.create_dataset("thickness",  measure.thickness)
        myfile.create_dataset("radius", measure.radius)
        myfile.create_dataset()
        
        for i in range(measure.thickness):
            radius_name = "radiusLists_"+str(i)
            myfile.create_dataset(radius_name, measure.r_list)
            distance_name = "distanceLists_"+str(i)
            myfile.create_dataset(distance_name, measure.d_list)
            WW_name = "distWW_"+str(i)
            myfile.create_dataset(WW_name, measure.dist_ww)
            
            plist_name = "clusterProperties_"+str(i)
            myfile.create_dataset(plist_name, measure.cluster_properties)
        myfile.close()
            
    def saveToTXT(self, measure, file_name):
        myfile = open(file_name, 'w+')
        myfile.write("time   thickness   Radius   Distance\n")
        
        for i, thick in enumerate(measure.thickness):
            myfile.write(str(i/1000.)+"   "
                         +thick+"   "
                         +measure.radius[i]+"   "
                         +measure.distance[i]+"\n"
                         )
        myfile.close()
        
        