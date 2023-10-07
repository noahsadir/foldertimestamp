# Folder Timestamp Tool

Script which affixes last-modified timestamps to folders.

## USAGE
This script is particularly effective on a folder whose
subdirectories follow a similar format (e.g. game saves)

### Arguments

Short | Long   | Description
------|--------| -----------
-p    | --path | The folder containing the subdirectories to rename
-e    |--eval  | The relative file path within a given subdirectory for which to evaluate the timestamp
-f    |--file  | (Optional) Only rename this specific subdirectory in the path

### Syntax

`python foldertimestamp.py -p [ABSPATH_CONTAINING_SUBDIRS] -e [RELPATH_OF_EVAL] -f(opt) [SUBDIR_NAME]`

## BACKGROUND
When archiving, it's often desired to attach timestamps
to help with organization, especially when making routine
backups of the same folder.

However, directory timestamps can often get messed up due
to how directories are copied. For example, a folder last
modified in 2014 and backed up in 2017 will have a timestamp
of 2017. The individual file timestamps, however, typically
remain intact.

This script helps alleviate this issue by evaluating a
specific file within a folder and assigning a date based on
when that file was last modified.

## EXAMPLE SCENARIO
Path `/Volumes/Backups/MinecraftSaves` contains the following:
- World1 (last played 2014-03-26)
- World2 (last played 2015-12-13)
- World3 (last played 2014-08-01)
These saves were all backed up on 2017-02-01 and thus each folder
claims to be last modified on that date.

So, if we run 
`python foldertimestamp.py -p /Volumes/Backups/MinecraftSaves -e level.dat`,
the script will scan the folder, look for `level.dat` within each
subdirectory and modify their names as such:
- 20140326_World1
- 20151213_World2
- 20140801_World3