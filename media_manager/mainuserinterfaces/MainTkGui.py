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
    from media_manager.guitemplates.tk.GenericTkGui import GenericTkGui
except ImportError:
    from guitemplates.tk.GenericTkGui import GenericTkGui


class MainTkGui(GenericTkGui):
    """
    Class that implements the Main GUI
    """

    def __init__(self, active_plugins):
        """
        Constructor
        :param active_plugins: The plugins to be displayed
        :return: void
        """
        self.plugins = active_plugins
        super().__init__("Main Gui")

    def lay_out(self):
        """
        Adds buttons for all plugins
        :return: void
        """
        i = 0
        row = 0
        column = -1
        while i < len(self.plugins):
            if i % 3 == 0 and not i == 0:
                row += 1
                column = 0
            else:
                column += 1

            def start_button_function(plugin):
                """
                The method run when pressed on the plugin button
                :param plugin: the plugin to which the button is assigned
                :return: void
                """
                plugin[0].start_gui(self)

            button = self.generate_simple_button(self.plugins[i].get_name(), start_button_function, self.plugins[i])
            button.grid(column=column, row=row)
            i += 1