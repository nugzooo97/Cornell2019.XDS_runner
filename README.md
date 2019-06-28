# Cornell2019.XDS_runner
Contain ALL 4 files to run XDS

###################################################     MAIN.py     ###################################################################

import os, argparse, fnmatch, h5py
from master import Master
			
def main():
	
	parser = argparse.ArgumentParser(description='Arguments required to process the data: input, beamcenter, distance.')
	
	parser.add_argument('-i', '--input', type=str, nargs='+', required=True, help='Path of Directory containing HDF5 master file(s)')
	
	parser.add_argument('-b', '--beamcenter', type=int, nargs=2, required=True, help='Beam center in X and Y')
	
	parser.add_argument('-r', '--oscillations', type=float, default=1, help='Oscillation angle per well')
	
	parser.add_argument('-d', '--distance', type=int, required=True, help='Detector distance in mm')
	
	parser.add_argument('-w', '--wavelength', type=float, default=1.216, help='Wavelength in Angstrom')
	
	parser.add_argument('-f', '--framesperdegree', type=int, default=5, help='Number of frames per degree')
	
	parser.add_argument('-t', '--totalframes', type=int, default=0, help='Total number of frames to be processed')
	
	parser.add_argument('--output', default=os.getcwd(), help='Use this option to change output directly')
	
	parser.add_argument('-sg', '--spacegroup', help='Space group')
	
	parser.add_argument('-u', '--unitcell', type=str, default="100 100 100 90 90 90", help='Unit cell')
	
	args = parser.parse_args()
	

	
	# We are going through each data file and creating a list called 'master_list' (defined in filter_master.py)
	# The list will store all master files
	
	for masterdir in args.input:
		master_list = fnmatch.filter(os.listdir(masterdir), "*master.h5")
		# Each element of the list now used to create an instance of a 'Master' class (defined in Master.py)
		for masterfile in master_list:
			# Return number of data files linked to a master file:
			print(masterfile)
			f = h5py.File("{a}/{b}".format(a=masterdir, b=masterfile))
			num_of_total_frames = len(f['/entry/data'])
			
			master_class = Master(args, masterfile, num_of_total_frames)
			master_class.create_and_run_Data_Wells()
		# We just generated empty directory(ies) named with respect to the master(s) files, 
		# AND returned the path to these directories

if __name__=='__main__':
	main()
  
  
#################################################     master.py     ####################################################################

import os, sys
from datawell import Datawell

class Master(object):

	# Generating a constructor:
	def __init__(self, args, masterpath, num_of_total_frames):
		self.args = args
		self.masterpath = masterpath
#		self.beamcenter = args.beamcenter
#		self.oscillations = args.oscillations
#		self.distance = args.distance
#		self.wavelength = args.wavelength
		self.frames_per_degree = args.framesperdegree
		self.total_frames = num_of_total_frames
		self.output = args.output
#		self.sg = args.spacegroup
#		self.uc = args.unitcell

		
		self.create_master_directory()


	def create_master_directory(self):
		try:
			end_index = self.masterpath.find('_master.h5')
			dir_name = self.masterpath[:end_index]
			new_dir_path = '{new_dir}/{name}'.format(new_dir = self.output, name = dir_name)
			try:
				os.makedirs(new_dir_path)
			except OSError:
				print("Creation of the directory {} failed. Such file may already exist.".format(dir_name))
			else:
				print("Successfully created the directory {}".format(dir_name))
		except:
			print("Something is not working. Check the code in 'Master.py'")
	
	def get_master_directory_path(self):
		end_index = self.masterpath.find('_master.h5')
		dir_name = self.masterpath[:end_index]
		new_dir_path = '{new_dir}/{name}'.format(new_dir = self.output, name = dir_name)
		return new_dir_path
	
	def create_and_run_Data_Wells(self):
		dir_path = self.get_master_directory_path()
		for framenum in range(1,self.total_frames,self.frames_per_degree):
			data_well = Datawell(framenum, framenum+self.frames_per_degree-1, dir_path, self.masterpath, self.args)
			data_well.setup_datawell_directory()

#################################################     datawell.py     ##################################################################

import subprocess, os
from generate_xds import gen_xds_text

class Datawell(object):
	
	def __init__(self, first_frame, last_frame, master_directory, masterpath, args):
		self.ff = first_frame
		self.lf = last_frame
		self.master_dir = master_directory
		self.masterpath = masterpath
		self.args = args
		
#		self.setup_datawell_directory()
		
	def setup_datawell_directory(self):
		frame_path = "{d}/{start}_{end}".format(d=self.master_dir, start=self.ff, end=self.lf)
		try:
			os.makedirs(frame_path)
		except OSError:
			print("Failed to create datawell directory")
		
		try:
			d_b_s_range = "{a} {b}".format(a=self.ff, b=self.lf)
			with open(os.path.join(frame_path, 'XDS.INP'), 'x') as input:
				input.write(gen_xds_text(self.args.unitcell, self.masterpath.replace("master", "??????"), 
				self.args.beamcenter[0], self.args.beamcenter[1], self.args.distance, self.args.oscillations, 
				self.args.wavelength, d_b_s_range, d_b_s_range, d_b_s_range))

		except:
			print("IO ERROR")
			
		os.chdir(frame_path)
		self.run()
		os.chdir(self.master_dir)


	
	def run(self):
		# run XDS in the datawell folder
		#change directory to the datawell directory - write a function for that
		subprocess.call(r"xds_par")
    
    
################################################     generate_xds.py     #############################################################

def gen_xds_text(UNIT_CELL_CONSTANTS, NAME_TEMPLATE_OF_DATA_FRAMES, ORGX, ORGY, DETECTOR_DISTANCE, OSCILLATION_RANGE, X_RAY_WAVELENGTH, DATA_RANGE, BACKGROUND_RANGE, SPOT_RANGE):
	text = """
	
SPACE_GROUP_NUMBER=0
UNIT_CELL_CONSTANTS= {in_1}
 
NAME_TEMPLATE_OF_DATA_FRAMES= {in_2}
JOB= XYCORR INIT COLSPOT IDXREF DEFPIX INTEGRATE CORRECT

ORGX= {in_3}  ORGY= {in_4}    
DETECTOR_DISTANCE= {in_5}  

OSCILLATION_RANGE= {in_6}
X-RAY_WAVELENGTH= {in_7}

DATA_RANGE= {in_8}
BACKGROUND_RANGE= {in_9}
SPOT_RANGE= {in_10}

DETECTOR=EIGER
MINIMUM_VALID_PIXEL_VALUE=0
OVERLOAD= 1048500  
SENSOR_THICKNESS=0.32
QX=0.075  QY=0.075
NX= 1030  NY= 1065  
UNTRUSTED_RECTANGLE=    0 1031    514  552

LIB=/nfs/chess/sw/macchess/dectris-neggia-centos6.so

TRUSTED_REGION=0.0 1.41

DIRECTION_OF_DETECTOR_X-AXIS= 1.0 0.0 0.0
DIRECTION_OF_DETECTOR_Y-AXIS= 0.0 1.0 0.0

MAXIMUM_NUMBER_OF_JOBS=4
MAXIMUM_NUMBER_OF_PROCESSORS=8  

ROTATION_AXIS= 0.0 -1.0 0.0
INCIDENT_BEAM_DIRECTION=0.0 0.0 1.0
FRACTION_OF_POLARIZATION=0.99
POLARIZATION_PLANE_NORMAL= 0.0 1.0 0.0

REFINE(IDXREF)=BEAM AXIS ORIENTATION CELL  ! POSITION
REFINE(INTEGRATE)= ! ORIENTATION POSITION BEAM CELL AXIS
REFINE(CORRECT)=POSITION BEAM ORIENTATION CELL AXIS

VALUE_RANGE_FOR_TRUSTED_DETECTOR_PIXELS= 6000 30000
! INCLUDE_RESOLUTION_RANGE=50 1.8

MINIMUM_I/SIGMA=50.0
CORRECTIONS= !

SEPMIN=4.0      
CLUSTER_RADIUS=2

	""".format(in_1=UNIT_CELL_CONSTANTS, in_2=NAME_TEMPLATE_OF_DATA_FRAMES, in_3=ORGX, in_4=ORGY,
	in_5=DETECTOR_DISTANCE, in_6=OSCILLATION_RANGE, in_7=X_RAY_WAVELENGTH, in_8=DATA_RANGE, in_9=BACKGROUND_RANGE,
	in_10=SPOT_RANGE)
	return text
