import argparse, fnmatch, os, h5py
import master

def main():

	parser = argparse.ArgumentParser(description='Arguments required to process the data: input, beamcenter, distance.')

	parser.add_argument('-i', '--input', type=str, nargs='+', required=True, help='Path of Directory containing HDF5 master file(s)')

	parser.add_argument('-b', '--beamcenter', type=int, nargs=2, required=True, help='Beam center in X and Y')

	parser.add_argument('-r', '--oscillations', type=float, default=1, help='Oscillation angle per well')

	parser.add_argument('-d', '--distance', type=float, required=True, help='Detector distance in mm')

	parser.add_argument('-w', '--wavelength', type=float, default=1.216, help='Wavelength in Angstrom')

	parser.add_argument('-f', '--framesperdegree', type=int, default=5, help='Number of frames per degree')

	parser.add_argument('--output', default=os.getcwd(), help='Use this option to change output directly')

	parser.add_argument('-sg', '--spacegroup', help='Space group')

	parser.add_argument('-u', '--unitcell', type=str, default="100 100 100 90 90 90", help='Unit cell')

	parser.parse_args()

	args = parser.parse_args()


	# We are going through each data file and creating a list called 'master_list' (defined in filter_master.py)
	# The list will store all master files

	for masterdir in args.input:
		master_list = fnmatch.filter(os.listdir(masterdir), "*master.h5")
		print(master_list)
		# Each element of the list now used to create an instance of a 'Master' class (defined in Master.py)
		for masterfile in master_list:
			# Return number of data files linked to a master file:
			masterpath = "{}/{}".format(masterdir, masterfile)
			parser.add_argument("-t","--totalframes", type=int, default=master.getNumberOfFiles_fast(masterpath),
			help="Total number of frames to be processed, default all")
			args = parser.parse_args()

			master_class = master.Master(args, masterpath, args.totalframes)
			master_class.create_and_run_Data_Wells()
		# We just generated empty directory(ies) named with respect to the master(s) files,
		# AND returned the path to these directories

if __name__=='__main__':
	main()
