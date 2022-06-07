import argparse
import subprocess, shlex
import os, sys
from pathlib import Path

#MEGAcmd commands are implemented as .bat files in its localappdata directory
megacmd_path = Path(os.environ.get('LOCALAPPDATA')) / 'MEGAcmd'

def parse_and_run(cmd_string):
	'''Given a command string, process it with shlex and run with subprocess'''
	exec_seq = shlex.split(cmd_string)
	#Uncomment below line to see backend commands that are being run
	#print(cmd_string)
	return subprocess.run(exec_seq, capture_output = True, text = True)

def run_mega_cmd(cmd, *args):
	cmd = '"' + (megacmd_path / f'mega-{cmd}.bat').as_posix() + '"'
	for arg in args:
		cmd += ' ' + arg

	return parse_and_run(cmd).stdout

def mega_login(session_id):
	return run_mega_cmd('login', session_id)

def mega_ls(path):
	return run_mega_cmd('ls', path)

def mega_find(path, pattern):
	found_files =  run_mega_cmd('find', f'"{path}"', f'--pattern="{pattern}"').split('\n')

	#process file list
	output = []
	for f in found_files:
		if f == '':
			continue
		if f.startswith('[API:err'):
			print(f'Error in output, dropping from filelist: {f}')
		output.append(f)
	
	return output

def mega_mv(*args, dest):
	return run_mega_cmd('mv', *args, f'"{dest}"')

def mega_cd(path='/'):
	return run_mega_cmd('cd', f'"{path}"')

def mega_cp(*args, dest):
	return run_mega_cmd('cp', *args, f'"{dest}"')

def mega_thumbnail(remote_path, local_path = None):
	'''Download the thumbnail for the remote file'''
	arg = f'"{remote_path}"'
	if local_path != None:
		arg += f' "{local_path}"'

	output = run_mega_cmd('thumbnail', arg)

	return output

if __name__ == "__main__":
	print(f'Not expected to be run by itself: {sys.argv[0]}')
	exit()