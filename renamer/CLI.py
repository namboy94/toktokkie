from renamer.utils.renamer import Renamer

"""
Class that models the CLI
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class CLI(object):

    """
    Constructor
    @:param directory - used if only a single directory is used
    """
    def __init__(self, directory=""):
        self.directory = directory

    """
    Starts the CLI, or renames the originally given directory and exits
    """
    def start(self):
        if self.directory:
            renamer = Renamer(self.directory)
            renamer.parseDirectory()
            renamer.requestConfirmation()
        else:
            print("cli")




"""
Showname
-Season X
--Quality
---Episode X
---Episode Y
---Episode Z
"""
