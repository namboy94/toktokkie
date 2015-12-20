from subprocess import Popen
"""
Class that handles the creation of Folders
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FolderCreator(object):

    """
    Constructor
    @:param parentDirectory - the parent directory of the new directory
    """
    def __init__(self, parentDirectory, name, seasons=0, ova=False, specials=False, extras=False, movies=False):
        self.parentDirectory = parentDirectory
        self.name = name
        self.directory = self.parentDirectory + "/" + self.name
        self.seasons = seasons
        self.ova = ova
        self.specials = specials
        self.extras = extras
        self.movies = movies

    """
    Creates the new directory
    """
    def create(self):
        Popen(["mkdir", self.directory])
        i = 1
        while i <= self.seasons:
            Popen(["mkdir", "-p", self.parentDirectory + "/Season " + str(i) + "/Quality"])
            i += 1
        if self.ova: Popen(["mkdir", self.directory + "/OVA"])
        if self.specials: Popen(["mkdir", "-p", self.directory + "/Specials/Quality"])
        if self.extras: Popen(["mkdir", "-p", self.directory + "/Extras/Quality"])
        if self.movies: Popen(["mkdir", "-p", self.directory + "/Movies/Quality"])