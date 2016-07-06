#!/usr/bin/env python

import os
import sys

def changeIcon(folderDirectory, iconDirectory):
    print "Changing Folder " + folderDirectory + "'s icon to " + iconDirectory    
    os.system("gvfs-set-attribute -t string '" + folderDirectory + "' metadata::custom-icon 'file://" + iconDirectory + "'")

def parseFolder(rootDirectory):
    
    returnList = []
    rootDirectoryContent = os.listdir(rootDirectory)
    
    for a in rootDirectoryContent:
                
        showDirectory = rootDirectory + a + "/"
        showDirectoryContent = os.listdir(showDirectory)
        folderIconDirectory = showDirectory + "Folder Icon/"
        
        for b in showDirectoryContent:    
            if b.lower() == "desktop.ini" or b.lower() == "thumbs.db" or b.endswith(".txt"): continue
            if b != "Folder Icon":
                innerDirectory = showDirectory + b + "/"
                innerDirectoryContent = os.listdir(innerDirectory)
                
                for c in innerDirectoryContent:
                    if c.lower() == "desktop.ini" or c.lower() == "thumbs.db" or c.endswith(".txt"): continue
                    if c.endswith("+"):
                        cedit = c[:-1]
                    else:
                        cedit = c    
                    qualityLanguageDirectory = innerDirectory + c + "/"
                    folderIcon = folderIconDirectory + cedit + ".png"
                    changeIcon(qualityLanguageDirectory, folderIcon)
                
                folderIcon = folderIconDirectory + b + ".png"
                changeIcon(innerDirectory, folderIcon)
            else:
                folderIcon = folderIconDirectory + "Folder.png"
                changeIcon(folderIconDirectory, folderIcon)
                
        folderIcon = folderIconDirectory + "Main.png"
        changeIcon(showDirectory, folderIcon)
      
    return returnList  
    
rootDirectory = (sys.argv[1])
if not rootDirectory.endswith("/"):
    rootDirectory = rootDirectory + "/"
print rootDirectory
if os.path.isdir(rootDirectory):
    parseFolder(rootDirectory)
else:
    print "Error, invalid directory"


