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
