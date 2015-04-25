'''
ParserCollection
collection of parsing methods.

Created on Apr 25, 2015
Modified on Apr 25, 2015

@author Hermann Krumrey
@version 1.1
'''

#imports
import os

"""
getActiveDirectory
returns the active directory in the config file
@param configFileLocation - the location of the configuration file
"""
def getActiveDirectory(configFileLocation):
    configFile = open(configFileLocation,"r")
    directoryPath = configFile.readline()
    configFile.close()
    return directoryPath

"""
directoryChangeParser
prompts for a change of the directory to be iconized
@param configFileLocation - the location of the configuration file
"""
def directoryChangeParser(configFileLocation):
    directoryPath = getActiveDirectory(configFileLocation)
    #Asks for a yes/no prompt
    print "Current active directory is %s" % (directoryPath)
    print "Do you want to change the directory? (y/n)"
    yesNoPrompt = True
    while yesNoPrompt is True:
        answer = raw_input("")
        if answer == "y":
            yesNoPrompt = False
            change = True
        elif answer == "n":
            yesNoPrompt = False
            change = False
        else:
            print "Input was not understood. Please enter \"y\" or \"n\":"
    #change the directory
    if change is True:
        print "Please enter the new directory:"
        directoryPrompt = True
        while directoryPrompt is True:
            newDirectory = raw_input("")
            if not newDirectory.endswith("/"):
                newDirectory = newDirectory + "/"
            
            if os.path.isdir(newDirectory):
                directoryPrompt = False
            else:
                print "This is not a valid directory, please try again."
        configFile = open(configFileLocation,"w")
        configFile.close()
        configFile = open(configFileLocation,"a")
        configFile.write(newDirectory)
        configFile.close()
        
"""
iconParser
parses through the parent folder of the folders whose icons should be changed and changes all their icons according
to conventions set by the author of this program.
@param rootDirectory - the parent directory to be parsed
@param warningFile - the location of a file that contains warnings that occur during parsing
"""
def iconParser(rootDirectory,warningFile):
    
    returnList = []
    rootDirectoryContent = os.listdir(rootDirectory)
    rootDirectoryContent.sort(key=lambda x: x)
    
    for a in rootDirectoryContent:
        
        if a.lower() == "desktop.ini" or a.lower() == "thumbs.db" or a.endswith(".txt"): continue
                
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
                    changeIcon(qualityLanguageDirectory, folderIcon, c, warningFile, folderIconDirectory)
                
                folderIcon = folderIconDirectory + b + ".png"
                changeIcon(innerDirectory, folderIcon, b, warningFile, folderIconDirectory)
            else:
                folderIcon = folderIconDirectory + "Folder.png"
                changeIcon(folderIconDirectory, folderIcon, "Folder", warningFile, folderIconDirectory)
                
        folderIcon = folderIconDirectory + "Main.png"
        changeIcon(showDirectory, folderIcon, "Main", warningFile, folderIconDirectory)
        
        completeCheck(folderIconDirectory, warningFile)
      
    return returnList

"""
changeIcon
changes a single folder icon and generates PNGs if necessary.
Also creates a warning file in the warnings.txt file if an ico file is over 1MB in size, often resulting in errors.
@param folderDirectory - the directory of the folder whose icon should be changed
@param iconDirectory - the full path name of the icon file
@param iconName - the name of the icon
@param warningFile - the location of the file that contains warnings
@param folderIconDirectory - the directory of all folder icons for thios particular show
"""
def changeIcon(folderDirectory, iconDirectory, iconName, warningFile, folderIconDirectory):
    if iconName.endswith("+"):
        iconName = iconName[:-1]
        iconDirectory = folderIconDirectory + iconName + ".png"
    if not os.path.isfile(iconDirectory):
        icoFile = folderIconDirectory + iconName + ".ico"
        pngFile = iconDirectory
        os.system("convert \"" + icoFile + "\" \"" + pngFile + "\"")
        newPngs = []
        for newIcon in os.listdir(folderIconDirectory):
            if newIcon.endswith(".png") and iconName in newIcon:
                newPngDir = folderIconDirectory + newIcon
                newPngs.append(newPngDir)
        newPngs.sort(key=lambda x: x)
        largestPNG = ""
        largestPNGSize = 0;
        for png in newPngs:
            if os.path.getsize(png) > largestPNGSize:
                largestPNG = png
                largestPNGSize = os.path.getsize(png)
        index = 0
        while index < len(newPngs):
            if newPngs[index] != largestPNG:
                os.system("rm \"" + newPngs[index] + "\"")
            else:
                os.system("mv \"" + newPngs[index] + "\" \"" + pngFile + "\"")
            index = index + 1
        if os.path.getsize(icoFile) > 1000000:
            workingWarningFile = open(warningFile, "a")
            workingWarningFile.write(icoFile + "\n")
            workingWarningFile.close()
    print "Changing Folder " + folderDirectory + "'s icon to " + iconDirectory    
    os.system("gvfs-set-attribute -t string '" + folderDirectory + "' metadata::custom-icon 'file://" + iconDirectory + "'")
    
"""
completeCheck
checks if every .ico file has a partner .png file.
@param folderIconDirectory - the directory of the folder icons
@param warningFile - the file in which warnings are saved.
"""
def completeCheck(folderIconDirectory,warningFile):
    icoArray = []
    for fil in os.listdir(folderIconDirectory):
        if fil.endswith(".ico"):
            icoArray.append(fil)
    for icoFile in icoArray:
        plainName = icoFile[:-4]
        pngName = plainName + ".png"
        hasPNG = False
        for fil in os.listdir(folderIconDirectory):
            if fil == pngName:
                hasPNG = True
        if not hasPNG:
            icoFile = folderIconDirectory + icoFile
            pngFile = folderIconDirectory + pngName
            os.system("convert \"" + icoFile + "\" \"" + pngFile + "\"")
            newPngs = []
            for newIcon in os.listdir(folderIconDirectory):
                if newIcon.endswith(".png") and plainName in newIcon:
                    newPngDir = folderIconDirectory + newIcon
                    newPngs.append(newPngDir)
            newPngs.sort(key=lambda x: x)
            largestPNG = ""
            largestPNGSize = 0;
            for png in newPngs:
                if os.path.getsize(png) > largestPNGSize:
                    largestPNG = png
                    largestPNGSize = os.path.getsize(png)
            index = 0
            while index < len(newPngs):
                if newPngs[index] != largestPNG:
                    os.system("rm \"" + newPngs[index] + "\"")
                else:
                    os.system("mv \"" + newPngs[index] + "\" \"" + pngFile + "\"")
                index = index + 1
            if os.path.getsize(icoFile) > 1000000:
                workingWarningFile = open(warningFile, "a")
                workingWarningFile.write(icoFile + "\n")
                workingWarningFile.close()
