import os
from gi.repository import Gtk
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI
from plugins.iconizer.utils.DeepIconizer import DeepIconizer

"""
GUI for the Iconizer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class IconizerGUI(GenericGUI):

    """
    Sets up all interface elements of the GUI
    """
    def setUp(self):

        self.directoryEntry = self.generateEntry("Enter Directory here", self.iconizeStart)
        self.grid.attach(self.directoryEntry, 0, 0, 3, 2)

        self.startButton = self.generateSimpleButton("Start", self.iconizeStart)
        self.grid.attach_next_to(self.startButton, self.directoryEntry, Gtk.PositionType.RIGHT, 1, 1)

        self.iconizerMethodComboBox = self.generateComboBox(["Nautilus", "Nemo"])
        self.grid.attach_next_to(self.iconizerMethodComboBox[0], self.startButton, Gtk.PositionType.BOTTOM, 1, 1)

    """
    Starts the iconizing process
    """
    def iconizeStart(self, widget):
        directory = self.directoryEntry.get_text()
        if not os.path.isdir(directory):
            self.messageBox("Not a directory!")
            return
        children = os.listdir(directory)
        multiple = True
        for child in children:
            if child == "Folder Icon":
                multiple = False
                break
        if not directory.endswith("/"):
            directory += "/"

        if multiple:
            for child in children:
                self.iconizeDir(directory + child)

    """
    Iconizes a single folder
    @:param - directory - the directory to be iconized
    """
    def iconizeDir(self, directory):
        method = self.getCurrentSelectedComboBox(self.iconizerMethodComboBox)
        hasIcons = False
        for subDirectory in os.listdir(directory):
            if subDirectory == "Folder Icon":
                hasIcons = True
                break
        if not hasIcons:
            print("Error, " + directory + " has no subdirectory \"Folder Icon\"")

        DeepIconizer(directory, method).iconize()