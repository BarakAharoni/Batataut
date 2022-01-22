# -*- coding: utf-8 -*-
"""
 Effective Autoruns Detection
 Find out which path in your file system running automaticly after restart => Autorun!
 Use the script as follow:
    1) Run and Restart: python batataut.py --spread --output <output-path> --restart
    2) View Results:    python batataut.py --results --output <output-path> 
    3) Cleanup:         python batataut.py --delete --output <output-path> 

 Copyright (c) 2022 Sun Obziler and Barak Aharoni.  All Rights Reserved.
"""
import win32api
import pickle 
import os, sys
import argparse
from shutil import copyfile
import datetime


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
# TODO: echo everything to the pickle file.
BATCH_SCRIPT ="""@echo off
echo %~f0 > {} 
"""

BATCH_NAME = "batataut{}.bat"

# Dump dictionary to pickle file.
def dumpDict(location_dict):
    global output_path
    with open(output_path, 'wb') as f:
        pickle.dump(location_dict, f)

# Load pickle to dictionary data
def loadDict():
    global output_path
    with open(output_path, 'rb') as f:
        data = pickle.load(f)
    return data

# Parsing and printing the dictionary data
def parseDict():
    location_dict = loadDict()
    print("\nThose files are running automaticly after restart:\n")
    for index, path in location_dict.items():
        print("\t{}".format(path))

# Get dictionary from pickle file, delete all generated bats.
def cleanup(pickle_path):
    print("\nStarting cleanup...\n")
    location_dict = loadDict()
    for index,path in location_dict.items():
        try:
            os.remove("{}\\{}".format(path,BATCH_NAME.format(index)))
        except:
            print("\tCould not remove: {}".format("{}\\{}".format(path,BATCH_NAME.format(index))))
        
# Create bat file
def createFile(outFolder,counter):
    timestamp = datetime.datetime.now()
    fileName = '{}\\{}_{}'.format(outFolder , BATCH_NAME.format(counter),timestamp) 
    with open(fileName, 'w') as openFile:
        openFile.write(BATCH_SCRIPT.format(fileName))

# List all the drives on this system
def findDrives():
    drives = win32api.GetLogicalDriveStrings()
    return  [x.rstrip("\\") for x in drives.split('\000') if x] 

# Spread the bat script to whole file system
def spreadBat():
    
    counter = 0 
    location_dict = {}
    drives = findDrives()
    
    for drive in drives:
        
        # Checks if the drive is available and exists
        if(os.path.exists(drive)):
            print("Spread batch script to {} drive...".format(drive))

            # Change directory to root drive
            if(drive == "D:"):

                os.chdir(drive)
                
                # Copy the bat script to every directory
                for root, dirs, files in os.walk("{}\\Barak\\scripts\\".format(drive), topdown = False): # TO CHANGE BACK
                    for name in dirs:
                        dstDir = os.path.join(root, name)

                        print( '{}\\{}'.format(dstDir , BATCH_NAME.format(counter)) )
                        try:
                            createFile(dstDir, counter)
                            location_dict[counter] = dstDir
                            counter += 1
                            
                        except:
                            print("\tCould not created Bat at: " + dstDir)
    #dumpDict(location_dict)

# Restart the system
def restartSystem():
    print("\nRestart system...")
    os.system("shutdown -t 0 -r -f")

# Help menu
def printHelp():
    print("""Use the script as follow:
    1) Run and Restart: python batataut.py --spread --output <output-path> --restart
    2) View Results:    python batataut.py --results --output <output-path> 
    3) Cleanup:         python batataut.py --delete --output <output-path> 
    """)

def main():
    print(BANNER)
    
    parser = argparse.ArgumentParser(description='Batataut - Effective Autoruns Detection')
    parser.add_argument('--output', help='Pickle output path')
    parser.add_argument('--results', help='Print resoults' , action='store_true')
    parser.add_argument('--spread', help='Spread the batch file', action='store_true')
    parser.add_argument('--restart', help='Reboot the system', action='store_true')
    parser.add_argument('--delete', help='Delete evidences', action='store_true')
    
    args = parser.parse_args()

    global output_path
    if args.output:
        output_path = args.output

    if args.spread:
        spreadBat()
        
    if args.restart:
        restartSystem()

    if args.results:
        parseDict()

    if args.delete:
        cleanup(args.output)

if __name__ == "__main__":
    main()
