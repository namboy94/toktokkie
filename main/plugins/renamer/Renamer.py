from plugins.genericPlugin.GenericPlugin import GenericPlugin
#from plugins.renamer.userInterfaces.RenamerGUI import RenamerGUI

class Renamer(GenericPlugin):

    def getName(self):
        return "Renamer"

    def startCLI(self, parentCLI):
        print("cli")

    def startGUI(self, parentGUI):
        parentGUI.root.withdraw()
        #RenamerGUI().start()
        parentGUI.root.deiconify()