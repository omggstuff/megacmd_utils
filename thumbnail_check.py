import megacmd_lib as m
import argparse
from pathlib import Path

def has_thumb(path):
	'''Try to download the thumbnail for the given file, return true or false depending on success'''
	output = m.mega_thumbnail(path, 'thumbcheck_temp.jpg')
	if output.startswith('Thumbnail for'): return True
	elif 'Failed to get thumbnail' in output: return False
	elif output == '':
		print(f'Error in thumbcheck: file does not exist on Mega: {path}')
		return False
	else:
		print(f'{path}: Unexpected output for thumbnail cmd: "{output}"')
		raise Exception

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description="Given a Mega filelist, tries to download each file's thumbnail; if it fails, logs it to an output .txt file")
	ap.add_argument('filelist', type=str, help='List of filenames to check for thumbnails')
	ap.add_argument('--output', default=None, required = False, help='Text file to output filelist to')
	args = ap.parse_args()

	filelist = Path(args.filelist)

	#generate output filename from input filelist
	if args.output == None:
		outfile = filelist.with_suffix('.badfiles.txt')	
	else:
		outfile = Path(args.output)
	outfile.touch(exist_ok=True) #create badfiles.txt if it doesn't exist

	#use textfile to save progress with this filelist
	progress_file = filelist.with_suffix('.progress.txt')
	#create file first time through
	if not progress_file.exists():
		progress_file.touch()
	#load file entry to resume with
	with open(progress_file) as f:
		resume_path = f.read().strip()

	#cd to root dir
	m.mega_cd()

	#specifying the encoding to handle unicode characters; didn't think we needed to do this still??
	with open(filelist, 'r', encoding='utf-8') as f:
		i = 0
		print(f'Starting thumbcheck')
		if resume_path: print(f'Resuming from previous thumbcheck, searching for file: {resume_path}')
		
		for line in f.readlines():
			i += 1
			to_check = line.strip()
			if to_check == '': continue

			if resume_path:
				#check if this line is the line to-resume
				if to_check != resume_path: continue
				else:
					resume_path = ''
					print(f'Found. Resuming thumbcheck')
					continue

			#periodic output
			if i % 100 == 0: print(f'Processing file #{i}') 
			
			if not has_thumb(to_check): #file has no thumbnail, is either corrupt or a filetype without thumbnail
				with open(outfile, 'a') as h:
					h.write(to_check + '\n')

			#save to progress log
			with open(progress_file, 'w') as p:
				p.write(to_check)

	print(f'Done processing {filelist}; check {outfile} for output')