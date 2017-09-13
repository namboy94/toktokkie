"""
LICENSE:
Copyright 2015,2016 Hermann Krumrey

This file is part of toktokkie.

    toktokkie is a program that allows convenient managing of various
    local media collections, mostly focused on video.

    toktokkie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    toktokkie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with toktokkie.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

import os
import json
from typing import Dict


class Base(object):
    """
    The base Media Type class. Implements common functions, JSON schema framework and automatic checks
    """

    def __init__(self, path: str):
        """
        Initializes a new Media Type object from a directory path
        :param path: The path for which to create the Media Type object
        """

        self.path = path
        self.info_file = os.path.join(path, ".meta", "info.json")
        with open(self.info_file, 'r') as info:
            self.info = json.loads(info.read())

        if not self.check_if_valid():
            raise AttributeError("Invalid JSON")

        # Media Type specific attributes
        # Child Constructors should generally also have some here
        self.type = self.info["type"]
        self.name = self.info["name"]
        self.tags = self.info["tags"]

    def check_if_valid(self) -> bool:
        """
        Checks if the loaded JSON information is valid for the specified Media Type
        :return: True if the JSON is valid, False otherwise
        """
        attrs = self.define_attributes()

        # Check if all required attributes exist and have the correct type
        for required in attrs["required"]:
            if required not in self.info:
                return False
            if type(self.info[required]) is not attrs["required"][required]:
                return False

        # Check if any optional attributes have the correct type
        for optional in attrs["optional"]:
            if type(self.info[optional]) is not attrs["required"][optional]:
                return False

        # Check that all extender attributes are valid parent attributes
        for extender in attrs["extenders"]:
            if extender in self.info:
                if type(self.info[extender]) is not attrs["extenders"][extender]:  # == is not dict
                    return False
                for extender_attr in self.info[extender]:
                    if extender_attr not in self.info:
                        return False
                    if type(self.info[extender][extender_attr]) is not type(self.info[extender_attr]):
                        return False

    def write_changes(self):
        """
        Writes the current class/instance variables to the JSON file
        :return: None
        """
        # Child classes will probably need to do this for all class/instance variables and call this method using super
        self.info["type"] = self.type
        self.info["name"] = self.name
        self.info["tags"] = self.tags
        with open(self.info_file, 'w') as j:
            j.write(json.dumps(self.info, sort_keys=True, indent=4, separators=(',', ': ')))

    # noinspection PyTypeChecker
    @staticmethod
    def define_attributes(additional: Dict[str, dict] = None) -> Dict[str, Dict[str, type]]:
        """
        Defines the attributes for a media type
        :param additional: Can be used (together with super) by child classes to add more attributes
        :return: A dictionary of required and optional attributes, as well as identifiers for extenders
        """
        attributes = {
            "required": {"type": str, "name": str, "tags": list},
            "optional": {},
            "extenders": {}
        }
        if additional is not None:
            attributes["required"].update(additional["required"])
            attributes["optional"].update(additional["optional"])
            attributes["extenders"].update(additional["extenders"])

        return attributes
