from gi.repository import Gtk
import easygui
from plugins.renamer.utils.Renamer import Renamer
from plugins.genericPlugin.userinterfaces.GenericGUI import GenericGUI

"""
GUI for the Renamer plugin
@author Hermann Krumrey<hermann@krumreyh.com>
"""
class RenamerGUI(GenericGUI):

    """
    Sets up all interface elements of the GUI
    """
    def setUp(self):
        Gtk.Window.__init__(self, title="Main GUI")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.startRename)
        hbox.pack_start(button, True, True, 0)

        self.entry = Gtk.Entry()
        self.entry.set_text("")
        hbox.pack_start(self.entry, True, True, 0)

    """
    Starts the renaming process
    """
    def startRename(self, dummy=""):
        try:
            absDir = self.entry.get_text()
            print(absDir)
            renamer = Renamer(absDir)
            confirmation = renamer.requestConfirmation()
            if self.confirmer(confirmation):
                renamer.confirm(confirmation)
                renamer.startRename()
        except Exception as e:
            if str(e) == "Not a directory":
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, str(e))
                dialog.run()
                dialog.destroy()
            else: raise e

    """
    Asks the user for confirmation before continuing the rename
    """
    def confirmer(self, confirmation):
        i = 0
        while i < len(confirmation[0]):
            message = "Rename\n"
            message += confirmation[0][i]
            message += "\nto\n"
            message += confirmation[1][i]
            message += "\n?"
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION, Gtk.ButtonsType.YES_NO, "Confirmation")
            dialog.format_secondary_text(message)
            response = dialog.run()
            dialog.destroy()
            if not response == Gtk.ResponseType.YES:
                return False
            i += 1
        return True