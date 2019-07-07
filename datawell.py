import subprocess, os, re
from generate_xds import gen_xds_text


class Datawell(object):

	def __init__(self, first_frame, last_frame, master_directory, masterpath, args):
		self.ff = first_frame
		self.lf = last_frame
		self.master_dir = master_directory
		self.masterpath = masterpath
		self.args = args
		self.results_dict = {}
		self.final_dict = {}


	def setup_datawell_directory(self):



		try:
			os.makedirs(frame_path)
		except OSError:
			print("Failed to create datawell directory")
		#END OF SETUP_DATAWELL_DIRECTORY


	def generate_datawell_dict(self):
		#generate and return datawell dict with all variables
		#if processed, then is_indexed=True

		# Adding the frame number to the dictionary:
		new_name = "{start} {end}".format(start=self.ff, end=self.lf)
		self.results_dict['frame_number']=new_name

		# Adding information about whether the file was processed or not:
		processed = os.path.exists('{a}/{b}'.format(a=frame_path,b='XDS_ASCII.HKL'))
		results_dict['is_processed']=processed
#NEW
		if processed:
			matching = 'NUMBER OF ACCEPTED OBSERVATIONS (INCLUDING SYSTEMATIC ABSENCES'
			with open('{a}/{b}'.format(a=frame_path, b='CORRECT.LP')) as file:
				for line in file:
					if matching in line:
						value = re.search(r'\d+',line)
#						results_dict['accepted_reflections']= int(value.group(0))
						results_dict['accepted_reflections']= value.group(0)
		else:
			results_dict['accepted_reflections'] = None
#NEW.END

		# Addding information about whether the file was indexed or not:
		def check():
			if os.path.exists('{a}/{b}'.format(a=frame_path,b='XDS_ASCII.HKL')):
				with open('{a}/{b}'.format(a=frame_path, b='IDXREF.LP')) as file:
					lines = file.readlines()
				text = '!!! ERROR'
				for text in lines:
					return False
				else:
					return True
			return False

		results_dict['is_indexed']=check()

		os.chdir(self.master_dir)

		final_dict['{a}_{b}'.format(a=self.ff, b=self.lf)]=results_dict
		return final_dict

	def run(self):
		# run XDS in the datawell folder
		#change directory to the datawell directory - write a function for that
		frame_path = "{d}/{start}_{end}".format(d=self.master_dir, start=self.ff, end=self.lf)
		os.chdir(frame_path)
		try:
			d_b_s_range = "{a} {b}".format(a=self.ff, b=self.lf)
			with open(os.path.join(frame_path, 'XDS.INP'), 'x') as input:
				input.write(gen_xds_text(self.args.unitcell, self.masterpath.replace("master", "??????"),
				self.args.beamcenter[0], self.args.beamcenter[1], self.args.distance, self.args.oscillations,
				self.args.wavelength, d_b_s_range, d_b_s_range, d_b_s_range))

		except:
			print("IO ERROR")
		subprocess.call(r"xds_par")
