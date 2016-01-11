from subprocess import Popen

"""
Class that iconizes folders for the Nemo and/or Nautilus file browsers
"""
class NautilusNemoIconizer(object):

    """
    Iconizes the folder
    """
    @staticmethod
    def iconize(directory, icon):
        Popen(["gvfs-set-attribute", "-t", "string", directory, "metadata::custom-icon", "file://" + icon + ".png"])