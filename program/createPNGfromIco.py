#!/usr/bin/env python

import os
import sys
    
    
rootDirectory = (sys.argv[1])
if not rootDirectory.endswith("/"):
    rootDirectory = rootDirectory + "/"
print rootDirectory
if not os.path.isdir(rootDirectory):
    print "Error, invalid directory"
    sys.exit(1)

for folder in os.listdir(rootDirectory):
    folderIconDir = rootDirectory + folder + "/Folder Icon/"
    for icon in os.listdir(folderIconDir):
        if icon.endswith(".ico"):
            pureFileName = icon[:-4]
            icoFile = folderIconDir + icon
            noExtFile = icoFile[:-4]
            pngFile = noExtFile + ".png"
            os.system("convert \"" + icoFile + "\" \"" + pngFile + "\"")
            newPngs = []
            for newIcon in os.listdir(folderIconDir):
                if newIcon.endswith(".png") and pureFileName in newIcon:
                    newIconDir = folderIconDir + newIcon
                    newPngs.append(newIconDir)
            newPngs.sort(key=lambda x: x)
            index = 0
            while index < len(newPngs):
                if index < (len(newPngs) - 1):
                    os.system("rm \"" + newPngs[index] + "\"")
                else: 
                    os.system("mv \"" + newPngs[index] + "\" \"" + pngFile + "\"")
                index = index + 1

