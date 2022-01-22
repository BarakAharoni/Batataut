# -*- coding: utf-8 -*-
"""
 Effective Autoruns Detection
 Find out which path in your file system running automaticly after restart => Autorun!
 Use the script as follows:
    1) Run and Restart: python batataut.py --spread --output <output-path> --restart 
    2) Cleanup:         python batataut.py --delete --output <output-path> 

 Copyright (c) 2022 Sun Obziler and Barak Aharoni.  All Rights Reserved.
"""
import win32api
import pickle 
import os
import sys
import argparse
from shutil import copyfile
import datetime
import glob



__version__ = '12.1.22'

BANNER = """
+----------------------------------------------------------------------+
|   Effective Autoruns Detection                                       |
|                                                                      |
|       ________       _____       _____              _____            |
|       ___  __ )_____ __  /______ __  /______ ____  ___  /_           |
|       __  __  |  __ `/  __/  __ `/  __/  __ `/  / / /  __/           |
|       _  /_/ // /_/ // /_ / /_/ // /_ / /_/ // /_/ // /_             |
|       /_____/ \__,_/ \__/ \__,_/ \__/ \__,_/ \__,_/ \__/             |
|                                                                      |                                                    
|                                                                      |
|                                                                      |
| Created by Barak Aharoni & Sun Obziler                               |      
+----------------------------------------------------------------------+

"""

BATCH_SCRIPT ="""@echo off
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%:%ldt:~10,2%:%ldt:~12,6%
echo script in path:     %~f0   ran at:   [%ldt%]  >> {} 
"""

BATCH_NAME = "batataut{}.bat"

        
# Create bat file
def createFile(outFolder,counter):
    global outputPath
    fileName = '{}\\{}'.format(outFolder , BATCH_NAME.format(counter)) 
    with open(fileName, 'w') as openFile:
        openFile.write(BATCH_SCRIPT.format(outputPath))

# List all the drives on this system
def findDrives():
    drives = win32api.GetLogicalDriveStrings()
    return  [x.rstrip("\\") for x in drives.split('\000') if x] 

# Spread the bat script to whole file system
def batWalk(deleteFlag):
    
    counter = 0 
    location_dict = {}
    drives = findDrives()
    
    for drive in drives:
        
        # Checks if the drive is available and exists
        if(os.path.exists(drive)):

            print("Spread batch script to {} drive...".format(drive))
            os.chdir(drive)
            
            # Copy the bat script to every directory
            for root, dirs, files in os.walk("{}\\".format(drive), topdown = False): 
                for name in dirs:
                    dstDir = os.path.join(root, name)

                    print( '{}\\{}'.format(dstDir , BATCH_NAME.format(counter)) )
                    
                    if deleteFlag:
                        try:
                            
                            toDelete = glob.glob("batataut*.bat")[0]
                            os.remove(os.path.join(dstDir,toDelete))
                        except:
                            print("\tCould not delete file: {}".format(toDelete))
                    else:
                        try:
                            createFile(dstDir, counter)
                            location_dict[counter] = dstDir
                            counter += 1
                            
                        except:
                            print("\tCould not created Bat at: " + dstDir)


# Restart the system
def restartSystem():
    print("\nRestart system...")
    os.system("shutdown -t 0 -r -f")

# Help menu
def printHelp():
    print("""Use the script as follows:
    1) Run and Restart: python batataut.py --spread --output <output-path> --restart
    2) Cleanup:         python batataut.py --delete --output <output-path> 
    """)

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description='Batataut - Effective Autoruns Detection')
    parser.add_argument('--output', help='Pickle output path')
    parser.add_argument('--spread', help='Spread the batch file', action='store_true')
    parser.add_argument('--restart', help='Reboot the system', action='store_true')
    parser.add_argument('--delete', help='Delete evidences', action='store_true')
    
    args = parser.parse_args()

    global output_path
    if args.output:
        outputPath = args.output

    if args.spread:
        batWalk(False)
        
    if args.restart:
        restartSystem()

    if args.delete:
        batWalk(True)

if __name__ == "__main__":
    main()
