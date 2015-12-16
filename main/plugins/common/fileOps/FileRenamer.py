import os
from subprocess import Popen

class FileRenamer(object):

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