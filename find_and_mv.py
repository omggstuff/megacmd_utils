import megacmd_lib as m
import argparse
import datetime

if __name__ == "__main__":
	ap = argparse.ArgumentParser(description='Find all of the files matching filenames in a filelist, and move them to the specified destination')
	ap.add_argument('filelist', type=str, help='List of filenames to move')
	ap.add_argument('destination', type=str, help='Destination to move files to')
	ap.add_argument('--chunk_size', type=int, default=10, help='Number of files to move with each command')
	args = ap.parse_args()

	arg = '' #the current to-move filelist we're building
	moves = [] #the total collection of all move commands to send
	i = 0 #the number of files in the current command

	with open(args.filelist) as f:
		lines = f.read().split('\n')

		for line in lines:
			if line == '': continue
			files = m.mega_find('/', line)
			if len(files) > 0:
				for f in files:
					arg += f'"{f}" ' #add files to current list
					i += 1
					if i >= args.chunk_size:
						moves.append(arg) #add current list to collection, blank the temp list, repeat
						arg = ''
						i = 0
		if arg != '':	moves.append(arg) #end of filelist, add whatever's leftover

	dest = args.destination

	m.mega_cd()
	print(f'Moving files to {dest}')
	for i, move in enumerate(moves):
		if i % 10 == 0:	print(f'Running move command #{i} of {len(moves)}')
		m.mega_mv(move, dest=dest)
	print('Done.')