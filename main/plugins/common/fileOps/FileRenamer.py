import os
from subprocess import Popen

"""
Class that contains static methods to help rename files
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class FileRenamer(object):

    """
    Renames a file to a new file name, keeping the extension and filepath.
    """
    @staticmethod
    def renameFile(file, newname):

        try:
            originalFileName = file.rsplit("/", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                originalFileName = file
            else:
                raise e
        try:
            extension = "." + originalFileName.rsplit(".", 1)[1]
        except Exception as e:
            if "list index out of range" in str(e):
                extension = ""
            else:
                raise e

        newFile = os.path.dirname(file) + "/" + newname + extension
        Popen(["mv", file, newFile])