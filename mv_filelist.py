import megacmd_lib as m
import argparse
import datetime

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='Move all the files in a filelist to the specified destination')
	ap.add_argument('filelist', type=str, help='List of files to move')
	ap.add_argument('destination', type=str, help='Destination to move files to')
	ap.add_argument('--chunk_size', type=int, default=10, help='Number of files to move with each command')
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
	print(f'Moving files to {dest}')
	for i, move in enumerate(moves):
		if i % 10 == 0:	print(f'Moving file #{i*10} of {len(moves)*10}')
		m.mega_mv(move, dest=dest)
	print('Done.')