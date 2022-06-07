import megacmd_lib as m
import argparse
import datetime

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='Copy all the files in a filelist to the specified destination')
	ap.add_argument('filelist', type=str, help='List of files to copy')
	ap.add_argument('destination', type=str, help='Destination to copy files to')
	ap.add_argument('--chunk_size', type=int, default=10, help='Number of files to copy with each command')
	args = ap.parse_args()

	files = ''
	moves = []
	i = 0
	with open(args.filelist) as f:
		lines = f.read().split('\n')

		for line in lines:
			if line == '': continue
			files += f'"{line}" '
			i += 1
			if i == args.chunk_size:
				moves.append(files)
				files = ''
				i = 0
		if files != '':	moves.append(files)

	dest = args.destination

	m.mega_cd()
	print(f'Copying files to {dest}')
	for i, move in enumerate(moves):
		if i % 10 == 0:	print(f'Copying file #{i*args.chunk_size} of {len(moves)*args.chunk_size}')
		m.mega_cp(move, dest=dest)
	print('Done.')