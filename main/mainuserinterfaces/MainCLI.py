"""
Copyright 2015,2016 Hermann Krumrey

This file is part of media-manager.

    media-manager is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    media-manager is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    media-manager is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with media-manager.  If not, see <http://www.gnu.org/licenses/>.
"""

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