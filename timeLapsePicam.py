#!/usr/bin/python

# timeLapsPicam.py - A simple way to take time-lapse photos with your rpi

import subprocess
import os
import time
from datetime import datetime
import sys

debugMode = True # True or False

# Set the location for saved pictures
filepath = "~/Documents"
filepath = os.path.expanduser(filepath) # Expand the user homedir if needed

# Prepare the filename prefix based on date/time
timestamp=datetime.now()
filenamePrefix = ("%04d%02d%02d-%02d%02d%02d" % (timestamp.year, timestamp.month, timestamp.day, timestamp.hour, timestamp.minute, timestamp.second))

# start sequence numbering to be used for filename when saving
frameCount = 0 

# Settings of the photos to save, max resolution of picam is 2592 x 1944 (1.33:1)
# image gets cropped aspect ratio changes (so i believe, when i made 1920x1080)
saveWidth   = 1024 # 2592 # 1296
saveHeight  = 768 # 1944 # 972
saveQuality = 15 # Set jpeg quality (0 to 100)
captureTimeDelay = 5 # Number of seconds between pictures (60 * 60 = 1 hour)

# If we need to flip image or whatever 
# example: "-hf" = Set horizontal flip of image; "-vf" = Set vertical flip
cameraSettings = ""

# Take picture and save image to disk
def saveImage(settings, width, height, quality):
    global frameCount
    if checkDirectory(filepath): # make sure path exists and is writeable
        filename = filepath + "/" + filenamePrefix + ("_%05d" % frameCount) + ".jpg"
        if (debugMode == False):
            subprocess.call("raspistill %s -w %s -h %s -t 200 -e jpg -q %s -n -o %s" % (settings, width, height, quality, filename), shell=True)
        print ("Captured %s" % filename)
        frameCount +=1 #increment frame counter

		
def checkDirectory(filepath):
    if os.path.isdir(filepath):
        if os.access(filepath, os.W_OK | os.X_OK):
            return True
        else:
            print "Problem: Can't write to dir: %s" % filepath
            return False
    else:
        print "Problem: Directory %s doesn't exist." % filepath
        return False

# Quit if path doesn't exist or isn't writeable      
if (checkDirectory(filepath) == False): 
    sys.exit()

# Reset last capture time
lastCapture = time.time()
    
### Here's the Loop ###
while (True):

    takePicture = False
    if time.time() - lastCapture > captureTimeDelay:
        takePicture = True
	
    if takePicture:
        lastCapture = time.time()
        saveImage(cameraSettings, saveWidth, saveHeight, saveQuality)