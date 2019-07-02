import os, os.path, json
from os import path

def main():
	main_dictionary = {}
	path_to_data = '/home/nnk28/processed_files/'
	for experiment in os.listdir(path_to_data):
#		if os.path.isdir(experiment):	
		full_path = '{}/{}'.format(path_to_data, experiment)
				
		for datawell_dir in os.listdir(full_path):
							
			frame_dictionary = {}
							
			# Adding the frame number to the dictionary:
			new_name = datawell_dir.replace('_', ' ')
			frame_dictionary['frame_number']=new_name
							
							
			# Adding information about whether the file was processed or not:
			processed = os.path.exists('{a}/{b}/{c}/{d}'.format(a=path_to_data, b=experiment, c=datawell_dir, d='XDS_ASCII.HKL'))
			frame_dictionary['is_processed']=processed
							
							
			# Addding information about whether the file was indexed or not:
			def check():
				if os.path.exists('{a}/{b}/{c}/{d}'.format(a=path_to_data, b=experiment, c=datawell_dir, d='IDXREF.LP')):
					with open('{a}/{b}/{c}/{d}'.format(a=path_to_data, b=experiment, c=datawell_dir, d='IDXREF.LP')) as file:
						lines = file.readlines()
					text = '!!! ERROR'
					for text in lines:
						return False
				else:
					return True
									
			frame_dictionary['is_indexed']=check()				
										
							
			# Merging frame dictionary with main dictionary:	
			main_dictionary[datawell_dir]=frame_dictionary
							
		with open('{}_DICTIONARY.txt'.format(experiment), 'w') as file:
			file.write(json.dumps(main_dictionary))
#		else:
#			continue

				
		
#	print(main_dictionary)
		
		
if __name__=='__main__':
	main()
