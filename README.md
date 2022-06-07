# megacmd_utils

A collection of python utility scripts to interface with the Windows version of the MEGAcmd tool. (https://github.com/meganz/MEGAcmd)

Requires first using the MEGAcmd shell to login to a valid MEGA account; afterwards, these scripts will interface with MEGAcmd's provided .bat files, using your cached logged-in session.

## Usage
Each script has a number of usable arguments; available options can be viewed by running each with `-h`.  
Note: should these scripts be interrupted in some way, the `MEGAcmd-server.exe` can become unstable and no longer contact the MEGA servers; force-closing it via your Task Manager or similar and restarting it will normally make the scripts functional again.

## build_filelist.py
Outputs a list of files on your MEGA account to an output text file.  
Due to limitations with MEGAcmd's `find` command, can only either do all files `.*`, or one file extension at a time i.e. `.jpg`  
This process is pretty quick.

Run with `python build_filelist <ext>`, optionally specifying a sub-folder under which to do the search with `--remote <path>`, or the output text file with `--output <filename>`.  
If output filename is not specified, will generate a filename with the form `filelist-<ext>-<timestamp>.txt`.

## thumbnail_check.py
Given an input filelist (as is returned from the previous script), check for whether each file has a thumbnail that can be downloaded.  
This is intended to be used as a proxy for finding invalid/corrupted files, with the assumption that broken images will not have a valid thumbnail. It is suggested you pre-filter your input list to include only files you expect *should* have thumbnails (i.e. images, videos, pdfs), as *all* files without valid thumbnails will be put into your output filelist, including those that would never have a thumbnail (i.e. text files).

Run with `python thumnail_check.py <filelist>`, optionally specify an output filename with `--output <filename>`.  
If not specified, output filename will default to `<filelist>.badfiles.txt`.  
Will also create a `thumbcheck_temp.jpg` file as an artifact of the thumbnail downloading process. This file will be re-used for each file.  

Note: the thumbnail download process takes a few seconds per file, and thus can add up to a sizeable amount of time with larger filelists.  

Has built-in resume function: script will keep track of which file it last checked, by saving to `<filelist>.progress.txt`. Should the process get interrupted somehow, running the script with the same input filelist will resume where it left off, instead of starting over.