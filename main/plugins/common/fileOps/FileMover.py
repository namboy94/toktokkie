import os
from subprocess import Popen

"""
Class that contains static methods to help move files
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FileMover(object):

    """
    Moves a file to a new location.
    """
    @staticmethod
    def moveFile(file, location):

        locationBackup = location
        if not location.endswith("/"): locationBackup += "/"
        fileName = file.rsplit("/", 1)[1]

        newFile = locationBackup + fileName

        Popen(["mv", file, newFile]).wait()
        return newFile