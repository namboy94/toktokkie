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

# imports
try:
    from Globals import Globals
except ImportError:
    from media_manager.Globals import Globals


class MainGUI(Globals.selected_grid_gui_framework):
    """
    Class that implements the Main GUI
    """

    def __init__(self, active_plugins) -> None:
        """
        Constructor
        :param active_plugins: The plugins to be displayed
        :return: void
        """
        self.plugins = active_plugins
        super().__init__("Media Manager Version " + Globals.version_no)

    def lay_out(self) -> None:
        """
        Adds buttons for all plugins
        :return: void
        """

        modulo_var = 3
        while len(self.plugins) % modulo_var != 0:
            modulo_var -= 1

        i = 0
        row = 0
        column = -1
        while i < len(self.plugins):
            if i % modulo_var == 0 and not i == 0:
                row += 1
                column = 0
            else:
                column += 1

            def start_button_function(widget, plugin):
                """
                The method run when pressed on the plugin button
                :param widget: the button that caused this action
                :param plugin: the plugin to which the button is assigned
                :return: void
                """
                if widget is not None:
                    plugin.start_gui(self)

            button = self.generate_button(self.plugins[i].get_name(), start_button_function, self.plugins[i])
            self.position_absolute(button, column, row, 1, 1)
            i += 1
