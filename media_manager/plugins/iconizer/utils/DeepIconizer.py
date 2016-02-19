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

import os
import platform

try:
    from media_manager.plugins.iconizer.utils.iconizers.NautilusNemoIconizer import NautilusNemoIconizer
except ImportError:
    from plugins.iconizer.utils.iconizers.NautilusNemoIconizer import NautilusNemoIconizer


class DeepIconizer(object):
    """
    Class that handles the iconization of a parent directory and its children
    """

    def __init__(self, directory, method):
        """
        Constructor
        :param directory: the parent directory
        :param method: the method of iconization to be used
        :return: void
        """
        self.directory = directory
        if not directory.endswith("/"): 
            self.directory += "/"

        self.concrete_iconizer = None
        if method == "Nautilus" or method == "Nemo":
            self.concrete_iconizer = NautilusNemoIconizer
        else:
            raise NotImplementedError("Iconizing Method not implemented")
        self.folder_icon_directory = self.directory + ".icons/"
        self.concrete_iconizer.iconize(self.folder_icon_directory, self.folder_icon_directory + "folder")

    def iconize(self, directory=None):
        """
        Starts the iconization process
        :param directory: the directory to iconize
        """
        if directory is None:
            directory = self.directory
            self.concrete_iconizer.iconize(directory, self.folder_icon_directory + "media_manager")

        children = self.get_children(directory)

        i = 0
        while i < len(children[0]) and i < len(children[1]):
            self.concrete_iconizer.iconize(children[1][i], self.folder_icon_directory + children[0][i])
            self.iconize(children[1][i])
            i += 1

    @staticmethod
    def get_children(directory):
        """
        Gets the names and directory paths of the children of a directory
        :param directory: the directory to be used
        :return: the names and directories as a list of length 2
        """
        children_names = os.listdir(directory)
        if ".icons" in children_names:
            children_names.remove(".icons")
        children_dirs = []
        for child in children_names:
            child_dir = directory + child + "/"
            if not os.path.isdir(child_dir):
                children_names.remove(child)
                continue
            children_dirs.append(child_dir)

        return [children_names, children_dirs]

    @staticmethod
    def get_iconizer_options():
        if platform.system() == "Linux":
            return ["Nautilus", "Nemo"]
        elif platform.system() == "Windows":
            return ["Windows"]
        else:
            return []
