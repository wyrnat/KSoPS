KSoPS - Kinetic Simulation of Particle Sputtering
*******************************************************

	Author: 	Sven-Jannik Wöhnert
	Contact:	jannik.woehnert@desy.de
	Supervisor:	stephan.roth@desy.de
	Website:	http://stash.desy.de/projects/P03
	git:		https://stash.desy.de/scm/p03/ksops.git
	
	
Requierements:
	- Python 2 (2.7 recommended)
	- h5py
	- numpy
	- scipy
	- pygame
	
	
Start:
	- Edit "KSoPS.py"
	- define a name for "exp_name"
	- configure "myinitvals"
	- close File and start simulation with "python KSoPS.py"
	

Runtime:
	- With pygame, images of simulation steps are created
	- data eg. radius or distance will be saved to "_params.txt"
	- events eg. nucleation will be saved to "_events.txt"