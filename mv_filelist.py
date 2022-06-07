import megacmd_lib as m
import argparse
import datetime

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='Move all the files in a filelist to the specified destination')
	ap.add_argument('filelist', type=str, help='List of files to move')
	ap.add_argument('destination', type=str, help='Destination to move files to')
	args = ap.parse_args()

	files = ''
	with open(args.filelist) as f:
		lines = f.read().split('\n')

		for line in lines:
			if line == '': continue
			files += f'"{line}" '

	dest = args.destination

	print(f'Moving files to {dest}')
	m.mega_mv(files, dest=dest)
	print('Done.')