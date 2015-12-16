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
        while True:
            userInput = input("User Input:\n").lower()
            if userInput in ["quit", "exit"]:
                break
            else:
                pluginToRun = None
                for plugin in self.plugins:
                    if userInput == plugin.getName().lower():
                        pluginToRun = plugin
                        break
                if pluginToRun is None:
                    print("User Input not understood")
                else:
                    pluginToRun.startCLI(self)