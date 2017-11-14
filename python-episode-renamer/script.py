"""
Copyright 2015-2017 Hermann Krumrey

This file is part of python-episode-renamer.

python-episode-renamer is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

python-episode-renamer is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with python-episode-renamer.  If not, see <http://www.gnu.org/licenses/>.
"""
#LINUX-ONLY

import sys
import os

showName = raw_input("Please enter the show's name:   ")
try:
    episodeNo = int(raw_input("Please enter the first episode's number   "))
    episodeAmountIn = int(raw_input("Please enter the total amount of episodes   "))
    episodeAmount = episodeAmountIn - (episodeNo - 1)
    if episodeAmount < 0:
        print "Invalid amount of episodes, the program will now halt."
        sys.exit(1)
    seasonNo = int(raw_input("Please enter the show's season number   "))
    if seasonNo < 10:
        seasonString = "0" + str(seasonNo)
    else:
        seasonString = str(seasonNo)
except TypeError:
    print "Please enter integer values for episodes and seasons."
    print "The program will now halt."
    sys.exit(1)
    
fileDirectory = raw_input("Please enter the directory of the files to be renamed   ")
if not fileDirectory.endswith("/"):
    fileDirectory = fileDirectory + "/"
if not os.path.isdir(fileDirectory):
    print "Invalid directory"
    sys.exit(1)
qualityAndLanguage = raw_input("Please enter the quality and language of the show. Blank for default   ")
if qualityAndLanguage == "":
    qualityAndLanguage = "default"
fileDirectoryContent = os.listdir(fileDirectory)
fileDirectoryContent.sort(key=lambda x: x)
newDirectory = fileDirectory + showName + "/Season " + str(seasonNo) + "/" + qualityAndLanguage + "/"
firstTerminal = "mkdir \"" + fileDirectory + showName + "\""
secondTerminal = "mkdir \"" + fileDirectory + showName + "/Season " + str(seasonNo) + "\""
thirdTerminal = "mkdir \"" + fileDirectory + showName + "/Season " + str(seasonNo) + "/" + qualityAndLanguage + "\""
os.system(firstTerminal)
os.system(secondTerminal)
os.system(thirdTerminal)

illegalCharacters = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
episodeNameList = []
episodeNumberStrings = []
for x in xrange(episodeNo, episodeAmountIn + 1):
    episodeName = raw_input("Please enter the episode name for episode " + str(x) + "   ")
    for illegalCharacter in illegalCharacters:
        if illegalCharacter in episodeName:
            episodeName = episodeName.replace(illegalCharacter, "")
    if episodeName.endswith("!") or episodeName.endswith("."):
        episodeName = episodeName + " "
    episodeNameList.append(episodeName)
    if x < 10:
        episodeNumberStrings.append("0" + str(x))
    else:
        episodeNumberStrings.append(str(x))
        
if len(episodeNameList) != len(fileDirectoryContent) or len(episodeNumberStrings) != len(fileDirectoryContent):
    print "Invalid Input, the amount of files in the directory do not match the user's input"
    sys.exit(1)

print "please review the input before proceeding."

index = 0
for x in episodeNumberStrings:
    originalFile = fileDirectory + fileDirectoryContent[index]
    extension = os.path.splitext(originalFile)[1]
    newFile = fileDirectory + showName + " - S" + seasonString + "E" + x + " - " + episodeNameList[index]  + extension
    terminalString = "mv \"" + originalFile + "\" \"" + newFile + "\""
    index = index + 1
    print x
    print originalFile
    print "->"
    print newFile
    print terminalString + "\n"

proceed = raw_input("Proceed? (y/n)")
if proceed != "y":
    print "process canceled"
    sys.exit(1)

index = 0
for x in episodeNumberStrings:
    originalFile = fileDirectory + fileDirectoryContent[index]
    extension = os.path.splitext(originalFile)[1]
    newFile = fileDirectory + showName + " - S" + seasonString + "E" + x + " - " + episodeNameList[index]  + extension
    terminalString = "mv \"" + originalFile + "\" \"" + newFile + "\""
    os.system(terminalString)
    newFileNewLocation = newDirectory + showName + " - S" + seasonString + "E" + x + " - " + episodeNameList[index]  + extension
    newTerminalString = "mv \"" + newFile + "\" \"" + newFileNewLocation + "\""
    os.system(newTerminalString)
    index = index + 1
    
