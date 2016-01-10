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
        self.folderIconDirectory = self.directory + "Folder Icon/"

    """
    Starts the iconization process
    """
    def iconize(self, directory=None):

        if directory is None:
            directory = self.directory

        children = self.getChildren(directory)

        i = 0
        while i < len(children[0]):
            self.concreteIconizer.iconize(children[1][i], self.folderIconDirectory + children[0][i] + ".png")
            self.iconize(children[1][i])
            i += 1


    """
    Gets the names and directory paths of the children of a directory
    @:param directory - the directory to be used
    @:return the names and directories as a list of length 2
    """
    def getChildren(self, directory):
        childrenNames = os.listdir(directory)
        childrenDirs = []
        for child in childrenNames:
            if child == "Folder Icon": childrenNames.remove(child); continue
            childDir = directory + child + "/"
            if not os.path.isdir(childDir): childrenNames.remove(child); continue
            else: childrenDirs.append(childDir)

        return [childrenNames, childrenDirs]