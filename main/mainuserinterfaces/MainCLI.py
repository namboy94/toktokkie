"""
Class that implements the Main CLI
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class MainCLI(object):

    """
    Constructor
    """
    def __init__(self, activePlugins):
        self.plugins = activePlugins


    """
    Starts the user interface
    """
    def start(self):
        print("Starting Media Manager\n")
        while True:
            userInput = input("What would you like to do?\n").lower()
            if userInput in ["quit", "exit"]:
                break
            elif userInput in ["help"]:
                self.__printhelp__()
            else:
                pluginToRun = None
                for plugin in self.plugins:
                    if userInput == plugin.getCommandName().lower():
                        pluginToRun = plugin
                        break
                if pluginToRun is None:
                    print("User Input not understood")
                else:
                    pluginToRun.startCLI(self)

    """
    Prints a help string to the console
    """
    def __printhelp__(self):
        print("help\nPrints this help message\n")
        print("quit|exit\nExits the program\n")
        for plugin in self.plugins:
            print(plugin.getCommandName())
            print("starts the " + plugin.getName() + " plugin\n")