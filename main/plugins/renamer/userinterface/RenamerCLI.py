from plugins.genericPlugin.userinterfaces.GenericCLI import GenericCLI
from plugins.renamer.utils.Renamer import Renamer

"""
CLI for the Renamer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerCLI(GenericCLI):

    """
    Constructor
    @:param directory - used if only a single directory is used
    """
    def __init__(self):
        print()

    """
    Starts the CLI, or renames the originally given directory and exits
    """
    def start(self):
        while True:
            userInput = input("Enter the absolute file path of the folder to be used for renaming")
            if userInput.lower() in ["exit", "quit"]: break
            self.renameLoop(userInput)

    """
    """
    def renameLoop(self, directory):
        renamer = Renamer(directory)
        confirmation = renamer.requestConfirmation()
        if self.confirmer(confirmation):
            renamer.confirm(confirmation)
            renamer.startRename()

    """
    """
    def confirmer(self, confirmation):
        print("Confirmation:")
        i = 0
        while i < len(confirmation[0]):
            print("\nrename")
            print(confirmation[0][i])
            print("to")
            print(confirmation[1][i])
            print("?")
            answer = ""
            while not answer.lower() in ["y", "n"]:
                answer = input("(y/n)")
                if answer == "n": return False
            i += 1
        return True