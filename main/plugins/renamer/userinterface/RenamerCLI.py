from plugins.genericPlugin.userinterfaces.GenericCLI import GenericCLI

"""
CLI for the Renamer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerCLI(GenericCLI):

    #TODO Actually implement the CLI

    def __init__(self):
        print()
        
    def start(self):
        while True:
            userInput = input("User Input:\n").lower()
            if userInput in ["quit", "exit"]:
                break
            else:
                print("User Input not understood")