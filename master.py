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
