"""
Copyright 2015-2018 Hermann Krumrey <hermann@krumreyh.com>

This file is part of toktokkie.

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
"""

import os
import json
from typing import Type, List, Dict
from toktokkie.metadata.exceptions import InvalidMetadataException
from toktokkie.metadata.types import MetaType, MetaPrimitive, CommaList, \
    StrCommaList, Str


class Base:
    """
    The Base Metadata class. It defines general metadata methods and
    common interfaces.
    """

    type = Str("base")
    """
    The type of the Metadata. Shoudl generally be overridden by child classes
    """

    # -------------------------------------------------------------------------
    # These Methods should be extended by subclasses
    # -------------------------------------------------------------------------

    @classmethod
    def generate_from_prompts(cls, directory: str,
                              extra_data: List[Dict[str, MetaType]] = None):
        """
        Generates a Metadata object based on user prompts
        This can and should be extended by child classes
        :param directory: The path to the directory for which to generate
                          the metadata
        :param extra_data: Additional data. to insert into the data dictionary.
                           May be used to make extending the method easier
        :return: The generated metadata object
        """
        name = os.path.basename(directory)
        print("Generating " + cls.type + " metadata for " + name)
        data = {
            "type": cls.type,
            "name": cls.prompt_user("Name", Str, Str(name)),
            "tags": cls.prompt_user("Tags", CommaList, CommaList([]))
        }

        if extra_data is not None:
            for extra in extra_data:
                for key, value in extra.items():
                    data[key] = value

        data = cls.jsonize_dict(data)
        return cls(data)

    def to_dict(self) -> dict:
        """
        Generates a JSON-compatible dictionary representation of the
        metadata object. Should be extended by child classes
        :return: The dictionary representation
        """
        return {
            "type": self.type,
            "name": self.name,
            "tags": self.tags
        }

    def __init__(self, json_data: Dict[str, any]):
        """
        Initializes the Metadata object. If the provided JSON data is incorrect
        (i.e. missing elements or invalid types), an InvalidMetadata exception
        will be thrown.
        :param json_data: The JSON dictionary to use
                          to generate the metadata object
        """
        try:
            self.name = Str(json_data["name"])
            self.tags = StrCommaList(json_data["tags"])
        except KeyError:
            raise InvalidMetadataException()

    # -------------------------------------------------------------------------

    @classmethod
    def from_json(cls, json_file: str):
        """
        Generates a Metadata object from a JSON file path
        :param json_file: The path to the JSON file
        :return: The generated metadata object
        """
        with open(json_file, "r") as f:
            data = json.load(f)
        return cls(data)

    def write(self, json_file: str):
        """
        Writes the metadata to a file in JSON format
        :param json_file: The path to the JSON file in
                          which to write the metadata
        :return: None
        """
        with open(json_file, "w") as f:
            f.write(json.dumps(
                self.jsonize_dict(self.to_dict()),
                sort_keys=True,
                indent=4,
                separators=(",", ": ")
            ))

    @staticmethod
    def jsonize_dict(data: Dict[str, MetaType]) -> dict:
        """
        Resolves all parameters of a dictionary and turns it into a
        json-compatible dictionary
        :param data: The dictionary resolve
        :return: The resolved JSON-compatible dictionary
        """
        for key, value in data.items():
            data[key] = value.to_json()
        return data

    @staticmethod
    def prompt_user(arg: str, arg_type: Type[MetaPrimitive],
                    default: MetaPrimitive = None) -> any:
        """
        Prompts a user for input.
        :param arg: The argument which the user is prompted for
        :param arg_type: The argument's type
        :param default: An optional default value,
                        used when the user enters nothing
        :return: The result of the prompt
        """

        prompt = arg + " "
        if default is not None:
            prompt += "(Default: " + str(default) + ")"
        prompt += ":   "

        while True:
            response = input(prompt)
            if not response and default is None:
                continue
            elif not response and default is not None:
                return default
            else:
                try:
                    return arg_type.parse(response)
                except ValueError:
                    print("Invalid input: " + response)
                    continue
