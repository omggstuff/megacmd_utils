import megacmd_lib as m
import argparse
import datetime

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='Searches for files on your MEGA account matching the given extension, and output a text filelist')
	ap.add_argument('ext', type=str, help='Extension of files to search for, i.e. ".jpg"')
	ap.add_argument('--remote', type=str, default='/', help='Remote subdirectory under which to search')
	ap.add_argument('--output', default=None, required = False, help='Text file to output filelist to')
	args = ap.parse_args()

	ext = args.ext

	#change to root dir
	m.mega_cd()
	found = m.mega_find(args.remote, f'*{ext}')

	if args.output == None:
		timeformat = "%Y%m%d-%H%M%S"
		timestr = datetime.datetime.now().strftime(timeformat)
		if '*' in ext: outfile = f"filelist-{timestr}.txt"
		else: outfile = f"filelist-{ext[1:]}-{timestr}.txt"
	else:
		outfile = args.output

	print(f'Found {len(found)} files, writing to output: {outfile}')

	with open(outfile, 'w') as f:
		for line in found:
			f.write(line + '\n')

	print(f'Finished writing output: {outfile}')