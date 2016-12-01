'''
Created on 02.03.2016

@author: jannik
'''
import h5py

class IOService(object):
    '''
    Save and load data files
    '''


    def __init__(self):
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
        myfile.write("Time\t")
        myfile.write("Thickness\t")
        myfile.write("Radius\t")
        myfile.write("Distance\t")
        myfile.write("Density\n")
        for i, thick in enumerate(measure.thickness):
            myfile.write(str(measure.time[i])+"\t"
                         +str(thick)+"\t"
                         +str(measure.radius[i])+"\t"
                         +str(measure.distance[i])+"\t"
                         +str(measure.cluster_density[i])+"\n"
                         )
        myfile.close()
        
    def saveEventsToTXT(self, measure, file_name):
        myfile = open(file_name, 'w+')
        myfile.write("Time\t")
        myfile.write("Thickness\t")
        myfile.write("Deposition_Substrat\t")
        myfile.write("Deposition_Cluster\t")
        myfile.write("Nucleation\t")
        myfile.write("Aggregation\t")
        myfile.write("Coalescence\n")
        for i, thick in enumerate(measure.thickness):
            myfile.write(str(measure.time[i])+"\t"
                         +str(thick)+"\t"
                         +str(measure.dist_ww[i]['deposition_sputter'])+"\t"
                         +str(measure.dist_ww[i]['clusterdeposition_sputter'])+"\t"
                         +str(measure.dist_ww[i]['nucleation'])+"\t"
                         +str(measure.dist_ww[i]['aggregation'])+"\t"
                         +str(measure.dist_ww[i]['coalescence'])+"\n"
                         )
        
        myfile.close()