"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
from plugins.iconizer.utils.iconizers.NautilusNemoIconizer import NautilusNemoIconizer

"""
Class that handles the iconization of a parent directory and its children
"""
class DeepIconizer(object):

    """
    Constructor
    @:param directory - the parent directory
    @:param method - the method of iconization to be used
    """
    def __init__(self, directory, method):
        self.directory = directory
        if not directory.endswith("/"): self.directory += "/"

        self.concreteIconizer = None
        if method == "Nautilus" or method == "Nemo":
            self.concreteIconizer = NautilusNemoIconizer
        else:
            raise NotImplementedError("Iconizing Method not implemented")
        self.folderIconDirectory = self.directory + ".icons/"
        self.concreteIconizer.iconize(self.folderIconDirectory, self.folderIconDirectory + "folder")

    """
    Starts the iconization process
    """
    def iconize(self, directory=None):

        if directory is None:
            directory = self.directory
            self.concreteIconizer.iconize(directory, self.folderIconDirectory + "main")

        children = self.getChildren(directory)

        i = 0
        while i < len(children[0]) and i < len(children[1]):
            self.concreteIconizer.iconize(children[1][i], self.folderIconDirectory + children[0][i])
            self.iconize(children[1][i])
            i += 1


    """
    Gets the names and directory paths of the children of a directory
    @:param directory - the directory to be used
    @:return the names and directories as a list of length 2
    """
    def getChildren(self, directory):
        childrenNames = os.listdir(directory)
        if ".icons" in childrenNames: childrenNames.remove(".icons")
        childrenDirs = []
        for child in childrenNames:
            childDir = directory + child + "/"
            if not os.path.isdir(childDir): childrenNames.remove(child); continue
            childrenDirs.append(childDir)

        return [childrenNames, childrenDirs]