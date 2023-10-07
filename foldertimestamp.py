# --- foldertimestamp.y ---
# Created by Noah Sadir on 2023-10-07
#
# Script which affixes last-modified timestamps to folders.
#
# ~~ USAGE ~~
# This script is particularly effective on a folder whose
# subdirectories follow a similar format (e.g. game saves)
# 
# Arguments
# -p/--path : The folder containing the subdirectories to rename
# -e/--eval : The relative file path within a given subdirectory for which to evaluate the timestamp
# -f/--file : (Optional) Only rename this specific subdirectory in the path
#
# RUN SYNTAX: `python foldertimestamp.py -p [ABSPATH_CONTAINING_SUBDIRS] -e [RELPATH_OF_EVAL] -f(opt) [SUBDIR_NAME]`
#
# ~~ BACKGROUND ~~
# When archiving, it's often desired to attach timestamps
# to help with organization, especially when making routine
# backups of the same folder.
#
# However, directory timestamps can often get messed up due
# to how directories are copied. For example, a folder last
# modified in 2014 and backed up in 2017 will have a timestamp
# of 2017. The individual file timestamps, however, typically
# remain intact.
#
# This script helps alleviate this issue by evaluating a
# specific file within a folder and assigning a date based on
# when that file was last modified.
#
# ~~ EXAMPLE SCENARIO ~~
# Path `/Volumes/Backups/MinecraftSaves` contains the following:
# - World1 (last played 2014-03-26)
# - World2 (last played 2015-12-13)
# - World3 (last played 2014-08-01)
# These saves were all backed up on 2017-02-01 and thus each folder
# claims to be last modified on that date.
# 
# So, if we run 
# `python foldertimestamp.py -p /Volumes/Backups/MinecraftSaves -e level.dat`,
# the script will scan the folder, look for `level.dat` within each
# subdirectory and modify their names as such:
# - 20140326_World1
# - 20151213_World2
# - 20140801_World3

import os
import os.path
import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path")
parser.add_argument("-e", "--eval")
parser.add_argument("-f", "--file")
args = parser.parse_args()

if args.path is None or args.eval is None:
    print("Please specify a path (-p/--path) and eval file (-e/--eval)")
    exit()

path = args.path
evalFile = args.eval
format = "%Y%m%d"

def init():
    try:
        successCount = 0
        failCount = 0
        # get list of subdirectories in path
        subdirs = [d for d in os.listdir(path) if not os.path.isfile(os.path.join(path, d))]
        for dir in subdirs:
            # if a single directory is targeted, ignore others
            if args.file is not None and dir == args.file:
                continue
            # ensure subdir is not some system/hidden folder
            # and that it contains the eval file
            filepath = os.path.join(path, dir, evalFile)
            if dir.startswith("."): continue
            if not os.path.isfile(filepath):
                print("Warning! '", filepath, "' is not a valid file!")
                failCount += 1
                continue
            # add modify date prefix to folder
            modificationDate = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            newdir = modificationDate.strftime(format) + "_" + dir
            # attempt to rename folder with timestamp prefix
            try:
                os.rename(os.path.join(path, dir), os.path.join(path, newdir))
            except:
                print("Warning! '", filepath, "' could not be renamed!")
                failCount += 1
                continue
            successCount += 1
        # output success metrics
        print("OPERATION COMPLETE")
        print("Success:", successCount)
        print("Failure:", failCount)
    except:
        print("'", path, "' is not a valid directory")

init()
