#!/usr/bin/env python
"""
Copyright 2015-2017 Hermann Krumrey

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

