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
        print(children)
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