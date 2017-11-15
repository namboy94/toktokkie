#!/usr/bin/env python
"""
Copyright 2015-2017 Hermann Krumrey <hermann@krumreyh.com>

This file is part of nautilus-foldericons.

nautilus-foldericons is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nautilus-foldericons is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with nautilus-foldericons.
If not, see <http://www.gnu.org/licenses/>.
"""


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


