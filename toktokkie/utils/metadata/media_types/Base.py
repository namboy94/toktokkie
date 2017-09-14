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
from typing import Dict, List


class Base(object):
    """
    The base Media Type class. Implements common functions, JSON schema framework and automatic checks
    """

    identifier = "base"
    """
    An identifier string that indicates the type
    """

    def __init__(self, path: str, generate: bool = False, overwrite_with_generated: bool = False):
        """
        Initializes a new Media Type object from a directory path
        :param path: The path for which to create the Media Type object
        :param generate: Can be set to True to generate the directory and a basic info.json file.
        :param overwrite_with_generated: Can be set to True to overwrite any existing info.json file while generating.
        """

        self.path = path
        self.info_file = os.path.join(path, ".meta", "info.json")

        if generate:
            metadir = os.path.join(self.path, ".meta")
            if not os.path.isdir(metadir):
                os.makedirs(metadir)
            if not os.path.isfile(self.info_file) or overwrite_with_generated:
                self.generate_info_file()

        with open(self.info_file, 'r') as info:
            self.info = json.loads(info.read())

        self.check_if_valid()

        # Media Type specific attributes
        # Child Constructors should generally also have some here
        self.type = self.info["type"]
        self.name = self.info["name"]
        self.tags = self.info["tags"]

        if self.type != self.identifier:
            raise AttributeError("Media Type Mismatch")

    def generate_info_file(self):
        """
        Generates a skeleton info.json file
        :return: None
        """
        data = {}
        attrs = self.define_attributes()
        for required in attrs["required"]:
            data[required] = attrs["required"][required]()
        data["type"] = self.identifier
        data["name"] = os.path.basename(self.path)
        with open(self.info_file, 'w') as f:
            f.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))

    def check_if_valid(self):
        """
        Checks if the loaded JSON information is valid for the specified Media Type
        If not, raise a descriptive AttributeError
        """
        attrs = self.define_attributes()

        # Check if all required attributes exist and have the correct type
        for required in attrs["required"]:
            if required not in self.info:
                raise AttributeError("Required Attribute " + required + " missing.")
            if type(self.info[required]) is not attrs["required"][required]:
                raise AttributeError("Attribute " + required + " has wrong type: " + str(type(self.info[required])))

        # Check if any optional attributes have the correct type
        for optional in attrs["optional"]:
            if optional in self.info and type(self.info[optional]) is not attrs["optional"][optional]:
                raise AttributeError("Invalid optional attribute: " + optional)

        # Check that all extender attributes are valid parent attributes
        for extender_type in attrs["extenders"]:
            if extender_type in self.info:

                if type(self.info[extender_type]) is not dict:
                    raise AttributeError("Extender Type is not a dictionary: " + extender_type)

                for extender in self.info[extender_type]:  # extender ~ 'Season 1'

                    if type(self.info[extender_type][extender]) is not attrs["extenders"][extender_type]:
                        raise AttributeError("Extender is not a dictionary: " + extender)

                    for extender_attr in self.info[extender_type][extender]:

                        if extender_attr not in self.info:
                            raise AttributeError("Invalid attribute defined in extender: " + extender_attr)

                        if not isinstance(
                                self.info[extender_type][extender][extender_attr],
                                type(self.info[extender_attr])):
                            raise AttributeError("Invalid type for extender attribute: " + extender_attr)

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

    def add_noneable_to_info(self, key: str, value: None or object):
        """
        Small helper method that makes it easier to update a None-able value in the info dictionary
        :param key: The key to update
        :param value: The value to update with
        :return: None
        """
        if value is not None:
            self.info[key] = value
        elif key in self.info:
            self.info.pop(key)

    # noinspection PyTypeChecker,PyDefaultArgument
    @staticmethod
    def define_attributes(additional: List[Dict[str, Dict[str, type]]]=[]) -> Dict[str, Dict[str, type]]:
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
        for extra in additional:
            attributes["required"].update(extra["required"])
            attributes["optional"].update(extra["optional"])
            attributes["extenders"].update(extra["extenders"])

        return attributes
