from plugins.genericPlugin.GenericPlugin import GenericPlugin
#from plugins.renamer.userInterfaces.RenamerGUI import RenamerGUI

"""
Class that handles renaming of episodes
"""
class Renamer(GenericPlugin):

    """
    @:return "Renamer"
    """
    def getName(self):
        return "Renamer"

    """
    Starts the CLI
    """
    def startCLI(self, parentCLI):
        print("cli")

    """
    Starts the GUI, while hiding the parent until finished
    """
    def startGUI(self, parentGUI):
        parentGUI.root.withdraw()
        #RenamerGUI().start()
        parentGUI.root.deiconify()